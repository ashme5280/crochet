from enum import Enum
from fastapi import APIRouter, Query, HTTPException
import math
from .sphere import YARN_INCHES_PER_STITCH, YARN_STITCH_HEIGHT_INCHES, YARN_STITCH_WIDTH_INCHES, YarnWeight, YARN_GRAMS_PER_YARD

router = APIRouter(prefix="/cylinder", tags=["Cylinders"])

def calculate_cylinder_metrics(height_rounds, total_stitch_count, weight_key, hook_size_mm, closed, target_stitches):
    """Calculates height, diameter, volume, and yarn requirements for a cylinder."""
    base_height = YARN_STITCH_HEIGHT_INCHES.get(weight_key, 0.28)
    stitch_height_in = base_height * (hook_size_mm / 3.5)

    # Cap rounds account for the increase/decrease tips
    cap_rounds = 4 if closed else 2
    total_effective_rounds = height_rounds + cap_rounds
    estimated_height_in = total_effective_rounds * stitch_height_in

    # Cylinder diameter based on target_stitches circumference
    base_width = YARN_STITCH_WIDTH_INCHES.get(weight_key, 0.25)
    stitch_width_in = base_width * (hook_size_mm / 3.5)
    physical_circumference_in = target_stitches * stitch_width_in
    estimated_diameter_in = physical_circumference_in / math.pi

    # Cylinder Volume: V = pi * r^2 * h
    radius_in = estimated_diameter_in / 2.0
    volume_cubic_in = math.pi * (radius_in ** 2) * estimated_height_in
    volume_cubic_cm = volume_cubic_in * 16.387064

    # Yarn calculations
    base_inches_per_st = YARN_INCHES_PER_STITCH[weight_key]
    hook_adjusted_inches_per_st = base_inches_per_st * (hook_size_mm / 3.5)
    total_yarn_yards = round((total_stitch_count * hook_adjusted_inches_per_st / 36) * 1.15, 1)
    total_yarn_meters = round(total_yarn_yards * 0.9144, 1)

    # Weight calculations
    grams_per_yard = YARN_GRAMS_PER_YARD.get(weight_key, 4.5)
    total_grams = total_yarn_yards * grams_per_yard
    total_ounces = total_grams / 28.3495

    vol_in_rounded = round(volume_cubic_in, 2)
    vol_cm_rounded = round(vol_in_rounded * 16.387064, 1)

    return {
        "diameter_inches": round(estimated_diameter_in, 2),
        "diameter_cm": round(estimated_diameter_in * 2.54, 1),
        "height_inches": round(estimated_height_in, 2),
        "height_cm": round(estimated_height_in * 2.54, 1),
        "volume_cubic_inches": vol_in_rounded,
        "volume_cubic_cm": vol_cm_rounded,
        "total_stitches_worked": total_stitch_count,
        "estimated_yarn_yards": total_yarn_yards,
        "estimated_yarn_meters": total_yarn_meters,
        "estimated_weight_grams": round(total_grams, 1),
        "estimated_weight_oz": round(total_ounces, 1)
    }

@router.get("/")
def get_cylinder_pattern(
    yarn_weight: YarnWeight = Query(YarnWeight.dk, description="Select your yarn weight category"),
    hook_size_mm: float = Query(3.0, gt=0),
    initial_stitches: int = Query(6, gt=0),
    target_stitches: int | None = Query(None, gt=0, description="Target maximum stitches around the cylinder belly"),
    max_diameter_inches: float | None = Query(None, gt=0, description="Target finished diameter in inches"),
    max_diameter_cm: float | None = Query(None, gt=0, description="Target finished diameter in centimeters"),
    height_rounds: int | None = Query(None, gt=0, description="Number of straight even body rounds"),
    max_height_inches: float | None = Query(None, gt=0, description="Target finished height in inches"),
    max_height_cm: float | None = Query(None, gt=0, description="Target finished height in centimeters"),
    closed: bool = Query(True, description="True to close the end with decreases, False to leave open")
):
    # 1. Validate Width/Diameter Options (Must provide exactly one)
    width_options = sum(1 for opt in [target_stitches, max_diameter_inches, max_diameter_cm] if opt is not None)
    if width_options > 1:
        raise HTTPException(
            status_code=400,
            detail="Please provide ONLY ONE of: 'target_stitches', 'max_diameter_inches', or 'max_diameter_cm'."
        )
    if width_options == 0:
        raise HTTPException(
            status_code=400,
            detail="You must provide a width option: 'target_stitches', 'max_diameter_inches', or 'max_diameter_cm'."
        )

    # 2. Validate Height Options (Must provide exactly one)
    height_options = sum(1 for opt in [height_rounds, max_height_inches, max_height_cm] if opt is not None)
    if height_options > 1:
        raise HTTPException(
            status_code=400,
            detail="Please provide ONLY ONE height option: 'height_rounds', 'max_height_inches', or 'max_height_cm'."
        )
    if height_options == 0:
        raise HTTPException(
            status_code=400,
            detail="You must provide a height option: 'height_rounds', 'max_height_inches', or 'max_height_cm'."
        )

    # --- Process Width / Diameter ---
    effective_diameter_inches = max_diameter_inches
    if max_diameter_cm is not None:
        effective_diameter_inches = max_diameter_cm / 2.54

    if effective_diameter_inches is not None:
        weight_key = yarn_weight.value.lower()
        base_width = YARN_STITCH_WIDTH_INCHES.get(weight_key, 0.25)
        stitch_width_in = base_width * (hook_size_mm / 3.5)

        target_circumference = effective_diameter_inches * math.pi
        raw_stitches = target_circumference / stitch_width_in
        target_stitches = round(raw_stitches / initial_stitches) * initial_stitches

    if target_stitches <= initial_stitches:
        raise HTTPException(status_code=400, detail="target_stitches (or calculated from diameter) must be greater than initial_stitches.")

    # --- Process Height ---
    weight_key = yarn_weight.value.lower()
    if weight_key not in YARN_INCHES_PER_STITCH:
        raise HTTPException(status_code=400, detail="Invalid yarn_weight.")

    effective_height_inches = max_height_inches
    if max_height_cm is not None:
        effective_height_inches = max_height_cm / 2.54

    if effective_height_inches is not None:
        base_height = YARN_STITCH_HEIGHT_INCHES.get(weight_key, 0.28)
        stitch_height_in = base_height * (hook_size_mm / 3.5)
        cap_rounds = 4 if closed else 2

        target_belly_height = effective_height_inches - (cap_rounds * stitch_height_in)
        height_rounds = round(target_belly_height / stitch_height_in)
        if height_rounds < 1:
            height_rounds = 1

    instructions = []
    total_stitch_count = 0
    current_round = 1
    current_stitches = initial_stitches

    # 1. Foundation (Magic Ring)
    instructions.append({
        "round": current_round, "phase": "foundation", "stitches_in_round": current_stitches,
        "instruction": f"Rnd {current_round}: Start {initial_stitches} sc in a Magic Ring. ({current_stitches} sts)"
    })
    total_stitch_count += current_stitches

    # 2. Round 2: All Increases (Doubles initial stitch count)
    current_round += 1
    current_stitches += initial_stitches
    instructions.append({
        "round": current_round, "phase": "increase", "stitches_in_round": current_stitches,
        "instruction": f"Rnd {current_round}: [inc] x {initial_stitches}. ({current_stitches} sts)"
    })
    total_stitch_count += current_stitches

    # 3. Subsequent Increase Rounds
    increment = initial_stitches
    step_count = 1
    while current_stitches < target_stitches:
        current_round += 1
        current_stitches += increment
        instructions.append({
            "round": current_round, "phase": "increase", "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: [sc in next {step_count} sts, inc] x {increment}. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches
        step_count += 1

    # 4. Straight Even Tube Body
    for _ in range(height_rounds):
        current_round += 1
        instructions.append({
            "round": current_round, "phase": "even_tube", "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: sc in each st around. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches

    # 5. Optional Decrease Phase (Only if closed=True)
    if closed:
        step_count -= 1
        # Continue standard decreases until down to 2 * initial_stitches (ready for final all-dec row)
        while current_stitches > (initial_stitches * 2):
            current_round += 1
            current_stitches -= increment
            instructions.append({
                "round": current_round, "phase": "decrease", "stitches_in_round": current_stitches,
                "instruction": f"Rnd {current_round}: [sc in next {step_count} sts, dec] x {increment}. ({current_stitches} sts)"
            })
            total_stitch_count += current_stitches
            step_count -= 1

        # 6. Final Round: All Decreases (Mirrors Round 2 to close the tip back down)
        current_round += 1
        current_stitches -= initial_stitches
        instructions.append({
            "round": current_round, "phase": "decrease", "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: [dec] x {initial_stitches}, fasten off and weave in tail. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches

    metrics = calculate_cylinder_metrics(height_rounds, total_stitch_count, weight_key, hook_size_mm, closed, target_stitches)

    return {
        "shape": "cylinder",
        "parameters": {
            "initial_stitches": initial_stitches,
            "target_stitches": target_stitches,
            "max_diameter_inches": max_diameter_inches,
            "max_diameter_cm": max_diameter_cm,
            "height_rounds": height_rounds,
            "max_height_inches": max_height_inches,
            "max_height_cm": max_height_cm,
            "closed": closed,
            "yarn_weight": yarn_weight.value,
            "hook_size_mm": hook_size_mm
        },
        "dimensions": metrics,
        "total_rounds": len(instructions),
        "pattern": instructions
    }

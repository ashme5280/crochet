from enum import Enum
from fastapi import APIRouter, Query, HTTPException
import math

router = APIRouter(prefix="/sphere", tags=["Spheres"])

class YarnWeight(str, Enum):
    fingering = "fingering"
    sport = "sport"
    dk = "dk"
    worsted = "worsted"
    bulky = "bulky"
    super_bulky = "super_bulky"

YARN_INCHES_PER_STITCH = {
    "fingering": 1.3, "sport": 1.8, "dk": 2.0,
    "worsted": 2.5, "bulky": 3.8, "super_bulky": 5.0
}

YARN_STITCH_HEIGHT_INCHES = {
    "fingering": 0.15,
    "sport": 0.20,
    "dk": 0.22,
    "worsted": 0.28,
    "bulky": 0.40,
    "super_bulky": 0.55
}

YARN_STITCH_WIDTH_INCHES = {
    "fingering": 0.18, "sport": 0.22, "dk": 0.25,
    "worsted": 0.30, "bulky": 0.42, "super_bulky": 0.58
}

# Average grams per yard for each weight category
YARN_GRAMS_PER_YARD = {
    "fingering": 2.5,
    "sport": 3.0,
    "dk": 3.5,
    "worsted": 4.5,
    "bulky": 6.5,
    "super_bulky": 9.0
}

def calculate_sphere_metrics(instructions, total_stitch_count, weight_key, hook_size_mm, max_stitches):
    base_width = YARN_STITCH_WIDTH_INCHES.get(weight_key, 0.25)
    stitch_width_in = base_width * (hook_size_mm / 3.5)

    physical_circumference_in = max_stitches * stitch_width_in
    estimated_diameter_in = physical_circumference_in / math.pi

    radius_in = estimated_diameter_in / 2.0
    volume_cubic_in = (4.0 / 3.0) * math.pi * (radius_in ** 3)
    volume_cubic_cm = volume_cubic_in * 16.387064  # use full precision constant

    base_inches_per_st = YARN_INCHES_PER_STITCH[weight_key]
    hook_adjusted_inches_per_st = base_inches_per_st * (hook_size_mm / 3.5)
    total_yarn_yards = round((total_stitch_count * hook_adjusted_inches_per_st / 36) * 1.15, 1)
    total_yarn_meters = round(total_yarn_yards * 0.9144, 1)

    # Calculate weight in grams and ounces
    grams_per_yard = YARN_GRAMS_PER_YARD.get(weight_key, 4.5)
    total_grams = total_yarn_yards * grams_per_yard
    total_ounces = total_grams / 28.3495  # 1 ounce = 28.3495 grams

    return {
        "diameter_inches": round(estimated_diameter_in, 2),
        "diameter_cm": round(estimated_diameter_in * 2.54, 1),
        "volume_cubic_inches": round(volume_cubic_in, 2),
        "volume_cubic_cm": round(volume_cubic_cm, 1),
        "total_stitches_worked": total_stitch_count,
        "estimated_yarn_yards": total_yarn_yards,
        "estimated_yarn_meters": total_yarn_meters,
        "estimated_weight_grams": round(total_grams, 1),
        "estimated_weight_oz": round(total_ounces, 1)
    }

@router.get("/")
def get_sphere_pattern(
    yarn_weight: YarnWeight = Query(YarnWeight.dk, description="Select your yarn weight category"),
    hook_size_mm: float = Query(3.00, gt=0),
    initial_stitches: int = Query(6, gt=0),
    max_stitches: int | None = Query(None, gt=0, description="Target maximum stitches around the belly"),
    max_diameter_inches: float | None = Query(None, gt=0, description="Target finished diameter in inches"),
    max_diameter_cm: float | None = Query(None, gt=0, description="Target finished diameter in centimeters")
):
    # Ensure the user provides exactly one sizing option, not more or less
    provided_options = sum(1 for opt in [max_stitches, max_diameter_inches, max_diameter_cm] if opt is not None)
    if provided_options > 1:
        raise HTTPException(
            status_code=400,
            detail="Please provide ONLY ONE of: 'max_stitches', 'max_diameter_inches', or 'max_diameter_cm'."
        )
    if provided_options == 0:
        raise HTTPException(
            status_code=400,
            detail="You must provide a target size using 'max_stitches', 'max_diameter_inches', or 'max_diameter_cm'."
        )

    # If centimeters were provided, convert them to inches first
    effective_diameter_inches = max_diameter_inches
    if max_diameter_cm is not None:
        effective_diameter_inches = max_diameter_cm / 2.54

    # If a diameter (inches or converted cm) is given, calculate max_stitches
    if effective_diameter_inches is not None:
        weight_key = yarn_weight.value.lower()
        base_width = YARN_STITCH_WIDTH_INCHES.get(weight_key, 0.25)
        stitch_width_in = base_width * (hook_size_mm / 3.5)

        target_circumference = effective_diameter_inches * math.pi
        raw_stitches = target_circumference / stitch_width_in

        # Round to the nearest multiple of initial_stitches
        max_stitches = round(raw_stitches / initial_stitches) * initial_stitches

    if max_stitches <= initial_stitches:
        raise HTTPException(status_code=400, detail="max_stitches (or calculated from diameter) must be greater than initial_stitches.")

    weight_key = yarn_weight.value.lower()
    if weight_key not in YARN_INCHES_PER_STITCH:
        raise HTTPException(status_code=400, detail="Invalid yarn_weight.")

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

    # 2. Round 2: All Increases
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
    while current_stitches < max_stitches:
        current_round += 1
        current_stitches += increment
        instructions.append({
            "round": current_round, "phase": "increase", "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: [sc in next {step_count} sts, inc] x {increment}. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches
        step_count += 1

    # 4. Even Belly Rounds
    even_rounds = step_count - 2
    if even_rounds < 0:
        even_rounds = 0

    for _ in range(even_rounds):
        current_round += 1
        instructions.append({
            "round": current_round, "phase": "even", "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: sc in each st around. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches

    # 5. Decrease Rounds
    step_count -= 1
    while current_stitches > (initial_stitches * 2):
        current_round += 1
        current_stitches -= increment
        instructions.append({
            "round": current_round, "phase": "decrease", "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: [sc in next {step_count} sts, dec] x {increment}. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches
        step_count -= 1

    # 6. Final Round: All Decreases
    current_round += 1
    current_stitches -= initial_stitches
    instructions.append({
        "round": current_round, "phase": "decrease", "stitches_in_round": current_stitches,
        "instruction": f"Rnd {current_round}: [dec] x {initial_stitches}, fasten off and weave in tail. ({current_stitches} sts)"
    })
    total_stitch_count += current_stitches

    metrics = calculate_sphere_metrics(instructions, total_stitch_count, weight_key, hook_size_mm, max_stitches)

    return {
        "shape": "sphere",
        "parameters": {
            "yarn_weight": yarn_weight.value,
            "hook_size_mm": hook_size_mm,
            "initial_stitches": initial_stitches,
            "max_stitches": max_stitches,
            "max_diameter_inches": max_diameter_inches,
            "max_diameter_cm": max_diameter_cm
        },
        "dimensions": metrics,
        "total_rounds": len(instructions),
        "pattern": instructions
    }

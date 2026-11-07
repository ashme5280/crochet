from enum import Enum
from fastapi import APIRouter, Query, HTTPException
import math

router = APIRouter(prefix="/cone", tags=["Cones"])

class YarnWeight(str, Enum):
    fingering = "fingering"
    sport = "sport"
    dk = "dk"
    worsted = "worsted"
    bulky = "bulky"
    super_bulky = "super_bulky"

class ConeShape(str, Enum):
    narrow = "narrow"     # 2 increases per round (pointy)
    medium = "medium"     # 3 increases per round (standard)
    wide = "wide"         # 5 increases per round (shallow/flared)

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

YARN_GRAMS_PER_YARD = {
    "fingering": 2.5, "sport": 3.0, "dk": 3.5,
    "worsted": 4.5, "bulky": 6.5, "super_bulky": 9.0
}

def calculate_cone_metrics(instructions, total_stitch_count, weight_key, hook_size_mm, max_stitches, cone_shape):
    base_width = YARN_STITCH_WIDTH_INCHES.get(weight_key, 0.25)
    stitch_width_in = base_width * (hook_size_mm / 3.5)

    physical_circumference_in = max_stitches * stitch_width_in
    estimated_base_diameter_in = physical_circumference_in / math.pi

    total_rounds = len(instructions)
    base_stitch_height = YARN_STITCH_HEIGHT_INCHES.get(weight_key, 0.22)
    hook_adjusted_stitch_height = base_stitch_height * (hook_size_mm / 3.5)
    calculated_height_inches = total_rounds * hook_adjusted_stitch_height

    base_inches_per_st = YARN_INCHES_PER_STITCH[weight_key]
    hook_adjusted_inches_per_st = base_inches_per_st * (hook_size_mm / 3.5)
    total_yarn_yards = round((total_stitch_count * hook_adjusted_inches_per_st / 36) * 1.15, 1)
    total_yarn_meters = round(total_yarn_yards * 0.9144, 1)

    grams_per_yard = YARN_GRAMS_PER_YARD.get(weight_key, 4.5)
    total_grams = total_yarn_yards * grams_per_yard
    total_ounces = total_grams / 28.3495

    return {
        "base_diameter_inches": round(estimated_base_diameter_in, 2),
        "base_diameter_cm": round(estimated_base_diameter_in * 2.54, 1),
        "height_inches": round(calculated_height_inches, 2),
        "height_cm": round(calculated_height_inches * 2.54, 1),
        "cone_shape": cone_shape.value,
        "total_stitches_worked": total_stitch_count,
        "estimated_yarn_yards": total_yarn_yards,
        "estimated_yarn_meters": total_yarn_meters,
        "estimated_weight_grams": round(total_grams, 1),
        "estimated_weight_oz": round(total_ounces, 1)
    }

@router.get("/")
def get_cone_pattern(
    yarn_weight: YarnWeight = Query(YarnWeight.dk, description="Select your yarn weight category"),
    hook_size_mm: float = Query(3.00, gt=0),
    cone_shape: ConeShape = Query(ConeShape.medium, description="Narrow, Medium, or Wide cone profile"),
    max_stitches: int | None = Query(None, gt=0, description="Target maximum stitches around the base"),
    max_diameter_inches: float | None = Query(None, gt=0, description="Target base diameter in inches"),
    max_diameter_cm: float | None = Query(None, gt=0, description="Target base diameter in centimeters"),
    stuffing: bool = Query(True, description="Include stuffing instructions")
):
    provided_diam_options = sum(1 for opt in [max_stitches, max_diameter_inches, max_diameter_cm] if opt is not None)
    if provided_diam_options > 1:
        raise HTTPException(status_code=400, detail="Please provide ONLY ONE of: 'max_stitches', 'max_diameter_inches', or 'max_diameter_cm'.")
    if provided_diam_options == 0:
        raise HTTPException(status_code=400, detail="You must provide a target base size using 'max_stitches', 'max_diameter_inches', or 'max_diameter_cm'.")

    if cone_shape == ConeShape.narrow:
        increment = 2
        initial_stitches = 4
    elif cone_shape == ConeShape.wide:
        increment = 5
        initial_stitches = 5
    else:
        increment = 3
        initial_stitches = 6

    effective_diameter_inches = max_diameter_inches
    if max_diameter_cm is not None:
        effective_diameter_inches = max_diameter_cm / 2.54

    weight_key = yarn_weight.value.lower()
    if weight_key not in YARN_INCHES_PER_STITCH:
        raise HTTPException(status_code=400, detail="Invalid yarn_weight.")

    if effective_diameter_inches is not None:
        base_width = YARN_STITCH_WIDTH_INCHES.get(weight_key, 0.25)
        stitch_width_in = base_width * (hook_size_mm / 3.5)
        target_circumference = effective_diameter_inches * math.pi
        raw_stitches = target_circumference / stitch_width_in
        max_stitches = round(raw_stitches / initial_stitches) * initial_stitches

    if max_stitches <= initial_stitches:
        raise HTTPException(status_code=400, detail="max_stitches (or calculated from diameter) must be greater than initial_stitches.")

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

# 2. Expansion Rounds (Fully explicit mathematical progression matching bracket format)
    step_count = 1
    while current_stitches < max_stitches:
        current_round += 1

        # Check what the standard next step would be
        next_stitches = current_stitches + increment

        if next_stitches >= max_stitches:
            # Directly calculate the exact sc count per bracket segment based on current stitches and max stitches
            # e.g., for 42 max sts from 39 sts with 3 increments: (42 - 39) / 3 = 1 increase per segment,
            # meaning total st per segment is 14 -> 12 sc + 1 inc = 14.
            segment_width = max_stitches // increment
            sc_per_bracket = segment_width - 2

            final_instruction = f"Rnd {current_round}: [sc in next {sc_per_bracket} sts, inc] x {increment}. ({max_stitches} sts)"
            if stuffing:
                final_instruction += " Stuff open cone firmly. Fasten off and leave a long tail for sewing to another piece."
            else:
                final_instruction += " Fasten off and leave a long tail for sewing to another piece."

            instructions.append({
                "round": current_round, "phase": "expansion", "stitches_in_round": max_stitches,
                "instruction": final_instruction
            })
            total_stitch_count += max_stitches
            current_stitches = max_stitches
            break

        current_stitches = next_stitches
        instructions.append({
            "round": current_round, "phase": "expansion", "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: [sc in next {step_count} sts, inc] x {increment}. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches
        step_count += 1

    metrics = calculate_cone_metrics(instructions, total_stitch_count, weight_key, hook_size_mm, max_stitches, cone_shape)

    stuffing_note = "Standard Poly-Fil. Note: This shape is an open cone, so the stuffing would happen right before it is attached to another piece - like attaching the tail to the body." if stuffing else "None"

    return {
        "shape": "cone",
        "parameters": {
            "yarn_weight": yarn_weight.value,
            "hook_size_mm": hook_size_mm,
            "cone_shape": cone_shape.value,
            "initial_stitches": initial_stitches,
            "max_stitches": max_stitches,
            "max_diameter_inches": max_diameter_inches,
            "max_diameter_cm": max_diameter_cm,
            "stuffing": stuffing
        },
        "dimensions": {
            "diameter_inches": metrics["base_diameter_inches"],
            "diameter_cm": metrics["base_diameter_cm"],
            "height_inches": metrics["height_inches"],
            "height_cm": metrics["height_cm"],
            "base_stitches": max_stitches
        },
        "supplies_you_need": {
            "estimated_yarn": f"{metrics['estimated_yarn_yards']} yards ({metrics['estimated_yarn_meters']} meters)",
            "hook": f"{hook_size_mm} mm",
            "stuffing_volume": stuffing_note
        },
        "total_rounds": len(instructions),
        "pattern": instructions
    }

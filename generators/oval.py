from enum import Enum
from fastapi import APIRouter, Query, HTTPException
import math

router = APIRouter(prefix="/oval", tags=["Ovals"])

class YarnWeight(str, Enum):
    fingering = "fingering"
    sport = "sport"
    dk = "dk"
    worsted = "worsted"
    bulky = "bulky"
    super_bulky = "super_bulky"

class OvalShape(str, Enum):
    pointed = "pointed"           # Tapers sharply at the ends
    egg_shaped = "egg_shaped"     # Fuller, rounded sides

YARN_INCHES_PER_STITCH = {
    "fingering": 1.3, "sport": 1.8, "dk": 2.0,
    "worsted": 2.5, "bulky": 3.8, "super_bulky": 5.0
}

YARN_STITCH_HEIGHT_INCHES = {
    "fingering": 0.15, "sport": 0.20, "dk": 0.22,
    "worsted": 0.28, "bulky": 0.40, "super_bulky": 0.55
}

YARN_STITCH_WIDTH_INCHES = {
    "fingering": 0.18, "sport": 0.22, "dk": 0.25,
    "worsted": 0.30, "bulky": 0.42, "super_bulky": 0.58
}

YARN_GRAMS_PER_YARD = {
    "fingering": 2.5, "sport": 3.0, "dk": 3.5,
    "worsted": 4.5, "bulky": 6.5, "super_bulky": 9.0
}

def calculate_oval_metrics(instructions, total_stitch_count, weight_key, hook_size_mm, max_length_in, max_width_in, oval_shape):
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
        "max_length_inches": round(max_length_in, 2),
        "max_length_cm": round(max_length_in * 2.54, 1),
        "max_width_inches": round(max_width_in, 2),
        "max_width_cm": round(max_width_in * 2.54, 1),
        "height_inches": round(calculated_height_inches, 2),
        "height_cm": round(calculated_height_inches * 2.54, 1),
        "oval_shape": oval_shape.value,
        "total_stitches_worked": total_stitch_count,
        "estimated_yarn_yards": total_yarn_yards,
        "estimated_yarn_meters": total_yarn_meters,
        "estimated_weight_grams": round(total_grams, 1),
        "estimated_weight_oz": round(total_ounces, 1)
    }

@router.get("/")
def get_oval_pattern(
    yarn_weight: YarnWeight = Query(YarnWeight.dk, description="Select your yarn weight category"),
    hook_size_mm: float = Query(3.00, gt=0),
    oval_shape: OvalShape = Query(OvalShape.egg_shaped, description="Pointed or Egg-shaped oval style"),
    max_length_inches: float | None = Query(None, gt=0, description="Target finished length in inches"),
    max_length_cm: float | None = Query(None, gt=0, description="Target finished length in cm"),
    max_width_inches: float | None = Query(None, gt=0, description="Target finished width in inches"),
    max_width_cm: float | None = Query(None, gt=0, description="Target finished width in cm"),
    max_height_inches: float | None = Query(None, gt=0, description="Target vertical height/depth in inches"),
    max_height_cm: float | None = Query(None, gt=0, description="Target vertical height/depth in cm"),
    stuffing: bool = Query(True, description="Include stuffing instructions")
):
    # Validate length options
    provided_len = sum(1 for opt in [max_length_inches, max_length_cm] if opt is not None)
    if provided_len > 1:
        raise HTTPException(status_code=400, detail="Provide ONLY ONE length option.")
    if provided_len == 0:
        raise HTTPException(status_code=400, detail="You must provide a target length.")

    # Automatically equate Width to Height if Width wasn't explicitly provided
    if max_width_inches is None and max_width_cm is None:
        if max_height_inches is not None:
            max_width_inches = max_height_inches
        elif max_height_cm is not None:
            max_width_cm = max_height_cm
        else:
            raise HTTPException(status_code=400, detail="You must provide a target width or height.")

    # Validate width options
    provided_wid = sum(1 for opt in [max_width_inches, max_width_cm] if opt is not None)
    if provided_wid > 1:
        raise HTTPException(status_code=400, detail="Provide ONLY ONE width option.")

    # Convert metrics to inches
    length_in = max_length_inches if max_length_inches is not None else (max_length_cm / 2.54)
    width_in = max_width_inches if max_width_inches is not None else (max_width_cm / 2.54)

    weight_key = yarn_weight.value.lower()
    base_width = YARN_STITCH_WIDTH_INCHES.get(weight_key, 0.25)
    stitch_w = base_width * (hook_size_mm / 3.5)

    target_stitches = round((2 * (length_in + width_in) * math.pi * 0.5) / stitch_w)
    if target_stitches < 16:
        target_stitches = 16

    instructions = []
    total_stitch_count = 0
    current_round = 1

    # 1. Foundation Round (e.g., 14 sts)
    starting_stitches = 14
    current_stitches = starting_stitches
    straight_sc_count = 4

    instructions.append({
        "round": current_round,
        "phase": "foundation",
        "stitches_in_round": current_stitches,
        "instruction": f"Rnd {current_round}: Ch 5, starting in the 2nd st from the hook: inc, sc {straight_sc_count}, inc. Continue around the other side of the chain with: inc, sc {straight_sc_count}, inc. ({current_stitches} sts)"
    })
    total_stitch_count += current_stitches

    # 2. Expansion Rounds (Adding 8 stitches per round)
    expansion_rounds = []
    rep_count = 1

    while current_stitches < target_stitches:
        current_round += 1
        current_stitches += 8

        inst = f"Rnd {current_round}: *(Sc {rep_count}, inc) x2, sc {straight_sc_count}, (inc, sc {rep_count}) x2. Repeat from the * once more. ({current_stitches} sts)"

        instructions.append({
            "round": current_round,
            "phase": "expansion",
            "stitches_in_round": current_stitches,
            "instruction": inst
        })
        expansion_rounds.append(inst)

        rep_count += 1
        total_stitch_count += current_stitches

    # 3. Even Body Rounds
    even_rounds = 3 if oval_shape == OvalShape.egg_shaped else 1
    for _ in range(even_rounds):
        current_round += 1
        instructions.append({
            "round": current_round,
            "phase": "even",
            "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: Sc {current_stitches}. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches

# 4. Decrease Rounds (Mirroring expansion down to the 14-stitch starting count)
    decrease_step = 0
    total_dec_rounds = len(expansion_rounds)

    for rev_inst in reversed(expansion_rounds):
        current_round += 1
        current_stitches -= 8  # Subtracts 8 stitches each round (e.g., 110 -> 102 -> 94...)
        decrease_step += 1

        # Clean the expansion instruction and turn 'inc' into 'dec'
        clean_inst = rev_inst.split(":", 1)[1] if ":" in rev_inst else rev_inst
        clean_inst = clean_inst.replace("inc", "dec")

        # Strip out the old stitch count from the copied string and replace with the new decremented count
        base_text = clean_inst.rsplit("(", 1)[0].strip()

        # If this is the very last decrease round, append the fasten-off language and match 14 sts
        if current_stitches == starting_stitches:
            dec_inst = f"Rnd {current_round}:{base_text} Fasten off with long tail, then pull yarn through each stitch in the round and tighten to close shape. ({current_stitches} sts)"
        else:
            dec_inst = f"Rnd {current_round}:{base_text} ({current_stitches} sts)"

        step_dict = {
            "round": current_round,
            "phase": "decrease",
            "stitches_in_round": current_stitches,
            "instruction": dec_inst
        }

        # Add stuffing prompt partway through the decrease rounds if stuffing is enabled
        if stuffing and decrease_step == max(1, total_dec_rounds // 2):
            step_dict["stuffing_instruction"] = "Start stuffing firmly here, adding more gradually as you shape before closing off."

        instructions.append(step_dict)
        total_stitch_count += current_stitches

    metrics = calculate_oval_metrics(
        instructions, total_stitch_count, weight_key, hook_size_mm, length_in, width_in, oval_shape
    )

    return {
        "shape": "oval",
        "parameters": {
            "yarn_weight": yarn_weight.value,
            "hook_size_mm": hook_size_mm,
            "oval_shape": oval_shape.value,
            "max_length_inches": max_length_inches,
            "max_length_cm": max_length_cm,
            "max_height_inches": max_height_inches,
            "max_height_cm": max_height_cm,
            "stuffing": stuffing
        },
        "dimensions": metrics,
        "supplies_you_need": {
            "estimated_yarn": f"{metrics['estimated_yarn_yards']} yards ({metrics['estimated_yarn_meters']} meters)",
            "hook": f"{hook_size_mm} mm",
            "stuffing_volume": "Standard Poly-Fil" if stuffing else "None"
        },
        "total_rounds": len(instructions),
        "pattern": instructions
    }

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

class SafetyEyesStyle(str, Enum):
    none = "None"
    standard = "Standard"
    kawaii = "Kawaii/Anime Style"
    minimalistic = "Minimalistic"

class StuffingOption(str, Enum):
    yes = "yes"
    no = "no"

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
    "fingering": 2.5,
    "sport": 3.0,
    "dk": 3.5,
    "worsted": 4.5,
    "bulky": 6.5,
    "super_bulky": 9.0
}

# Standard US & Metric Hook Label Mapping
HOOK_LABEL_MAP = {
    2.0: "B-1 (2.00mm)",
    2.25: "B-1 (2.25mm)",
    2.5: "C-2 (2.50mm)",
    2.75: "C-2 / D-3 (2.75mm)",
    3.0: "D-3 (3.00mm)",
    3.25: "D-3 (3.25mm)",
    3.5: "E-4 (3.50mm)",
    3.75: "F-5 (3.75mm)",
    4.0: "G-6 (4.00mm)",
    4.25: "G-6 (4.25mm)",
    4.5: "7 (4.50mm)",
    5.0: "H-8 (5.00mm)",
    5.5: "I-9 (5.50mm)",
    6.0: "J-10 (6.00mm)",
    6.5: "K-10.5 (6.50mm)",
    8.0: "L-11 (8.00mm)",
    9.0: "M-13 (9.00mm)",
    10.0: "N-14 (10.00mm)"
}

def get_hook_label(hook_mm: float) -> str:
    closest_size = min(HOOK_LABEL_MAP.keys(), key=lambda x: abs(x - hook_mm))
    if abs(closest_size - hook_mm) <= 0.15:
        return HOOK_LABEL_MAP[closest_size]
    return f"({hook_mm:.2f}mm)"

def calculate_sphere_metrics(total_stitch_count, weight_key, hook_size_mm, max_stitches, stuffing: str):
    base_width = YARN_STITCH_WIDTH_INCHES.get(weight_key, 0.25)
    stitch_width_in = base_width * (hook_size_mm / 3.5)

    physical_circumference_in = max_stitches * stitch_width_in
    estimated_diameter_in = physical_circumference_in / math.pi

    radius_in = estimated_diameter_in / 2.0
    volume_cubic_in = (4.0 / 3.0) * math.pi * (radius_in ** 3)
    volume_cubic_cm = volume_cubic_in * 16.387064

    base_inches_per_st = YARN_INCHES_PER_STITCH[weight_key]
    hook_adjusted_inches_per_st = base_inches_per_st * (hook_size_mm / 3.5)
    total_yarn_yards = round((total_stitch_count * hook_adjusted_inches_per_st / 36) * 1.15, 1)
    total_yarn_meters = round(total_yarn_yards * 0.9144, 1)

    grams_per_yard = YARN_GRAMS_PER_YARD.get(weight_key, 4.5)
    total_grams = total_yarn_yards * grams_per_yard
    total_ounces = total_grams / 28.3495

    polyfill_oz = round(volume_cubic_in * 0.12, 1) if stuffing.lower() == 'yes' else 0.0

    return {
        "diameter_inches": round(estimated_diameter_in, 2),
        "diameter_cm": round(estimated_diameter_in * 2.54, 1),
        "volume_cubic_inches": round(volume_cubic_in, 2),
        "volume_cubic_cm": round(volume_cubic_cm, 1),
        "total_stitches_worked": total_stitch_count,
        "estimated_yarn_yards": total_yarn_yards,
        "estimated_yarn_meters": total_yarn_meters,
        "estimated_weight_grams": round(total_grams, 1),
        "estimated_weight_oz": round(total_ounces, 1),
        "polyfill_stuffing_oz": polyfill_oz
    }

@router.get("/")
def get_sphere_pattern(
    yarn_weight: YarnWeight = Query(YarnWeight.dk, description="Select your yarn weight category"),
    hook_size_mm: float = Query(5.00, gt=0, description="Numeric hook size in mm for calculations"),
    safety_eyes: SafetyEyesStyle = Query(SafetyEyesStyle.standard, description="Safety eyes style preference"),
    stuffing: StuffingOption = Query(StuffingOption.yes, description="Include stuffing yes or no"),
    initial_stitches: int = Query(6, gt=0),
    max_stitches: int | None = Query(None, gt=0, description="Target maximum stitches around the belly"),
    max_diameter_inches: float | None = Query(None, gt=0, description="Target finished diameter in inches"),
    max_diameter_cm: float | None = Query(None, gt=0, description="Target finished diameter in centimeters")
):
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

    effective_diameter_inches = max_diameter_inches
    if max_diameter_cm is not None:
        effective_diameter_inches = max_diameter_cm / 2.54

    if effective_diameter_inches is not None:
        weight_key = yarn_weight.value.lower()
        base_width = YARN_STITCH_WIDTH_INCHES.get(weight_key, 0.25)
        stitch_width_in = base_width * (hook_size_mm / 3.5)

        target_circumference = effective_diameter_inches * math.pi
        raw_stitches = target_circumference / stitch_width_in
        max_stitches = round(raw_stitches / initial_stitches) * initial_stitches

    if max_stitches <= initial_stitches:
        raise HTTPException(status_code=400, detail="max_stitches (or calculated from diameter) must be greater than initial_stitches.")

    weight_key = yarn_weight.value.lower()
    if weight_key not in YARN_INCHES_PER_STITCH:
        raise HTTPException(status_code=400, detail="Invalid yarn_weight.")

    raw_instructions = []
    total_stitch_count = 0
    current_round = 1
    current_stitches = initial_stitches

    # 1. Foundation
    raw_instructions.append({
        "round": current_round, "phase": "foundation", "stitches_in_round": current_stitches,
        "instruction": f"Rnd {current_round}: Start {initial_stitches} sc in a Magic Ring. ({current_stitches} sts)"
    })
    total_stitch_count += current_stitches

    # 2. Round 2: All Increases
    current_round += 1
    current_stitches += initial_stitches
    raw_instructions.append({
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
        raw_instructions.append({
            "round": current_round, "phase": "increase", "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: [sc in next {step_count} sts, inc] x {increment}. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches
        step_count += 1

    # 4. Even Belly Rounds
    even_rounds = step_count - 2
    if even_rounds < 0:
        even_rounds = 0

    even_rounds_list = []
    for _ in range(even_rounds):
        current_round += 1
        even_rounds_list.append({
            "round": current_round, "phase": "even", "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: sc in each st around. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches

    # 5. Decrease Rounds
    decrease_rounds_list = []
    step_count -= 1
    while current_stitches > (initial_stitches * 2):
        current_round += 1
        current_stitches -= increment
        decrease_rounds_list.append({
            "round": current_round, "phase": "decrease", "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: [sc in next {step_count} sts, dec] x {increment}. ({current_stitches} sts)",
            "stitches_count": current_stitches
        })
        total_stitch_count += current_stitches
        step_count -= 1

    # 6. Final Round
    current_round += 1
    current_stitches -= initial_stitches
    final_instruction_text = f"Rnd {current_round}: [dec] x {initial_stitches}. Fasten off leaving a long tail and pull tail through all stitches and tighten to close shape. ({current_stitches} sts)"
    total_stitch_count += current_stitches

    metrics = calculate_sphere_metrics(total_stitch_count, weight_key, hook_size_mm, max_stitches, stuffing.value)

    # --- SIZING MATRIX LOOKUP BASED ON EQUATOR STITCHES ---
    if max_stitches <= 24:
        base_eye_mm, base_spacing = 7, 4
    elif max_stitches <= 30:
        base_eye_mm, base_spacing = 9, 5
    elif max_stitches <= 42:
        base_eye_mm, base_spacing = 11, 7
    elif max_stitches <= 54:
        base_eye_mm, base_spacing = 14, 10
    elif max_stitches <= 66:
        base_eye_mm, base_spacing = 16, 13
    else:
        base_eye_mm, base_spacing = 20, 16

    style_lower = safety_eyes.value.lower()
    if "kawaii" in style_lower or "anime" in style_lower:
        eye_size_mm = base_eye_mm + 2
        eye_spacing_st = base_spacing + 1
    elif "minimalistic" in style_lower:
        eye_size_mm = max(6, base_eye_mm - 2)
        eye_spacing_st = max(2, base_spacing - 1)
    else:
        eye_size_mm = base_eye_mm
        eye_spacing_st = base_spacing
    # ----------------------------------------------------

    # --- CALCULATE ROW TARGETS FOR SAFETY EYES ---
    if even_rounds_list:
        middle_even_index = len(even_rounds_list) // 2
        middle_even_round_num = even_rounds_list[middle_even_index]["round"]
        last_even_round_num = even_rounds_list[-1]["round"]
    else:
        middle_even_round_num = raw_instructions[-1]["round"]
        last_even_round_num = raw_instructions[-1]["round"]

    eye_target_row_from = middle_even_round_num - 1
    eye_target_row_to = middle_even_round_num
    # ----------------------------------------------

    final_instructions = []
    stuffing_triggered = False

    is_eyes_enabled = safety_eyes != SafetyEyesStyle.none and safety_eyes.value.lower() != "none"

    for item in raw_instructions + even_rounds_list + decrease_rounds_list:
        instr = item["instruction"]

        # Inject safety eyes instructions ONLY if safety eyes is enabled
        if is_eyes_enabled and even_rounds_list and item["round"] == last_even_round_num:
            base_text = instr.rsplit(" (", 1)[0]
            stitch_suffix = f" ({instr.rsplit(' (', 1)[1]}"
            instr = f"{base_text}. Insert safety eyes between rows {eye_target_row_from} and {eye_target_row_to}, count {eye_spacing_st} stitches apart.{stitch_suffix}"

        # Stuffing triggered strictly if stuffing option is 'yes'
        if stuffing.value.lower() == "yes" and not stuffing_triggered and item["phase"] == "decrease":
            if item["stitches_in_round"] == 24:
                instr += " Start stuffing, adding more gradually as you shape before closing off."
                stuffing_triggered = True

        final_instructions.append({
            "round": item["round"],
            "phase": item["phase"],
            "stitches_in_round": item.get("stitches_in_round"),
            "instruction": instr
        })

    final_instructions.append({
        "round": current_round,
        "phase": "decrease",
        "stitches_in_round": current_stitches,
        "instruction": final_instruction_text
    })

    formatted_hook_label = get_hook_label(hook_size_mm)

    supplies_you_need = {
        "estimated_yarn": f"{metrics['estimated_yarn_yards']} yards ({metrics['estimated_yarn_meters']} meters)",
        "hook": formatted_hook_label,
        "safety_eyes": f"2 safety eyes in {eye_size_mm}mm size ({safety_eyes.value} style)" if is_eyes_enabled else "None",
        "stuffing_volume": f"{metrics['polyfill_stuffing_oz']} oz of polyfill stuffing" if stuffing.value.lower() == 'yes' else "None (Unstuffed)"
    }

    return {
        "shape": "sphere",
        "supplies_you_need": supplies_you_need,
        "parameters": {
            "yarn_weight": yarn_weight.value,
            "hook_label": formatted_hook_label,
            "hook_size_mm": hook_size_mm,
            "safety_eyes": safety_eyes.value if is_eyes_enabled else "None",
            "stuffing": stuffing.value,
            "initial_stitches": initial_stitches,
            "max_stitches": max_stitches,
            "max_diameter_inches": max_diameter_inches,
            "max_diameter_cm": max_diameter_cm
        },
        "dimensions": metrics,
        "total_rounds": len(final_instructions),
        "pattern": final_instructions
    }

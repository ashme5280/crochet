from fastapi import FastAPI, Query, HTTPException

app = FastAPI(
    title="Amigurumi Sphere Generator with Precise Yardage",
    description="Calculates row-by-row crochet instructions, physical dimensions, and exact yarn yardage.",
    version="1.2.0"
)

# Standard average inches consumed per 1 single crochet (sc) by yarn weight
YARN_INCHES_PER_STITCH = {
    "fingering": 1.3,
    "sport": 1.8,
    "dk": 2.0,
    "worsted": 2.5,
    "bulky": 3.8,
    "super_bulky": 5.0
}

# Accurate vertical stitch height (inches) per yarn weight using tight amigurumi tension
YARN_STITCH_HEIGHT_INCHES = {
    "fingering": 0.10,
    "sport": 0.13,
    "dk": 0.15,
    "worsted": 0.18,
    "bulky": 0.25,
    "super_bulky": 0.35
}

@app.get("/sphere/")
def get_sphere_pattern(
    initial_stitches: int = Query(6, gt=0, description="Starting stitch count, e.g., magic ring of 6"),
    max_stitches: int = Query(24, gt=0, description="Maximum circumference stitch count at the widest part"),
    yarn_weight: str = Query("worsted", description="Yarn weight category (fingering, sport, dk, worsted, bulky, super_bulky)"),
    hook_size_mm: float = Query(3.5, gt=0, description="Crochet hook size in millimeters (e.g., 3.5, 4.0)")
):
    """Generates row-by-row crochet instructions, precise physical dimensions, and true yarn yardage estimates."""

    if max_stitches <= initial_stitches:
        raise HTTPException(
            status_code=400,
            detail="max_stitches must be greater than initial_stitches to build a sphere."
        )

    weight_key = yarn_weight.lower()
    if weight_key not in YARN_INCHES_PER_STITCH:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid yarn_weight. Choose from: {list(YARN_INCHES_PER_STITCH.keys())}"
        )

    instructions = []
    total_stitch_count = 0  # To track exact stitches for yardage
    current_round = 1
    current_stitches = initial_stitches

    # 1. Foundation Round
    instructions.append({
        "round": current_round,
        "phase": "foundation",
        "stitches_in_round": current_stitches,
        "instruction": f"Rnd {current_round}: Start {initial_stitches} sc in a Magic Ring. ({current_stitches} sts)"
    })
    total_stitch_count += current_stitches

    # 2. Increase Phase
    increment = initial_stitches
    step_count = 1

    while current_stitches < max_stitches:
        current_round += 1
        current_stitches += increment
        sc_count = step_count
        instructions.append({
            "round": current_round,
            "phase": "increase",
            "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: [sc in next {sc_count} st(s), inc] x {increment}. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches
        step_count += 1

    # 3. Even Phase (Cylindrical belly)
    even_rounds = step_count - 1
    for _ in range(even_rounds):
        current_round += 1
        instructions.append({
            "round": current_round,
            "phase": "even",
            "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: sc in each st around. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches

    # 4. Decrease Phase
    step_count -= 1
    while current_stitches > initial_stitches:
        sc_count = step_count
        current_round += 1
        current_stitches -= increment
        instructions.append({
            "round": current_round,
            "phase": "decrease",
            "stitches_in_round": current_stitches,
            "instruction": f"Rnd {current_round}: [sc in next {sc_count} st(s), dec] x {increment}. ({current_stitches} sts)"
        })
        total_stitch_count += current_stitches
        step_count -= 1

    # --- Precise Dimension & Yardage Calculations ---
    base_height = YARN_STITCH_HEIGHT_INCHES.get(weight_key, 0.18)
    stitch_height_in = base_height * (hook_size_mm / 3.5)

    # A sphere's diameter derived from the vertical span/total rounds
    approximate_total_rounds = len(instructions)
    estimated_diameter_in = approximate_total_rounds * stitch_height_in * 0.55
    estimated_diameter_cm = estimated_diameter_in * 2.54

    # Calculate exact inches of yarn consumed by every single stitch made
    base_inches_per_st = YARN_INCHES_PER_STITCH[weight_key]
    hook_adjusted_inches_per_st = base_inches_per_st * (hook_size_mm / 3.5)

    total_yarn_inches = total_stitch_count * hook_adjusted_inches_per_st
    total_yarn_yards_raw = total_yarn_inches / 36

    # Add a 15% safety buffer for magic ring tails, fastening off, and weaving ends
    total_yarn_yards_with_buffer = round(total_yarn_yards_raw * 1.15, 1)

    return {
        "parameters": {
            "initial_stitches": initial_stitches,
            "max_stitches": max_stitches,
            "yarn_weight": yarn_weight,
            "hook_size_mm": hook_size_mm
        },
        "estimated_dimensions": {
            "diameter_inches": round(estimated_diameter_in, 2),
            "diameter_cm": round(estimated_diameter_cm, 1),
            "total_stitches_worked": total_stitch_count,
            "estimated_yarn_yards": total_yarn_yards_with_buffer
        },
        "total_rounds": len(instructions),
        "pattern": instructions
    }

@app.get("/")
def root():
    return {"message": "Welcome to the Amigurumi Sphere Generator! Visit /docs to test the API."}

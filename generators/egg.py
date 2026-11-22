import math
from enum import Enum
from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Query
from constants import (
    YarnWeight,
    StuffingOption,
    CM_PER_INCH,
    YARN_INCHES_PER_STITCH,
    YARN_STITCH_HEIGHT_INCHES,
    YARN_STITCH_WIDTH_INCHES,
    YARN_GRAMS_PER_YARD,
    get_hook_label,
)

router = APIRouter(prefix="/egg", tags=["Egg"])

STANDARD_EGG_ASPECT_RATIO = 1.38  # Classic egg height-to-width proportion
EGG_SKEW_FACTOR = 0.22            # Places widest equator ~62% down from top


class ShellMode(str, Enum):
    whole = "Whole shell"
    split = "Split in half"


@router.get("/")
def get_egg_pattern(
    yarn_weight: YarnWeight = Query(YarnWeight.dk, description="Select your yarn weight category"),
    hook_size_mm: float = Query(3.0, gt=0, description="Numeric hook size in mm for calculations"),
    max_diameter_inches: Optional[float] = Query(None, gt=0, description="Target max egg diameter in inches"),
    max_diameter_cm: Optional[float] = Query(None, gt=0, description="Target max egg diameter in centimeters"),
    max_diameter_stitches: Optional[int] = Query(None, gt=0, description="Target max stitches around the widest equator"),
    shell_mode: ShellMode = Query(ShellMode.whole, description="Whole shell or Split in half at the widest equator"),
    stuffing: StuffingOption = Query(StuffingOption.yes, description="Include stuffing (only applies to Whole shell)"),
):
    # Ensure exactly ONE diameter input is provided (matches sphere.py validation)
    provided_options = sum(
        1 for opt in [max_diameter_inches, max_diameter_cm, max_diameter_stitches] if opt is not None
    )
    if provided_options > 1:
        raise HTTPException(
            status_code=400,
            detail="Please provide ONLY ONE of: 'max_diameter_inches', 'max_diameter_cm', or 'max_diameter_stitches'."
        )
    if provided_options == 0:
        raise HTTPException(
            status_code=400,
            detail="You must provide a target width using 'max_diameter_inches', 'max_diameter_cm', or 'max_diameter_stitches'."
        )

    weight_key = yarn_weight.value.lower()
    hook_factor = hook_size_mm / 3.5

    stitch_width_in = YARN_STITCH_WIDTH_INCHES[weight_key] * hook_factor
    stitch_height_in = YARN_STITCH_HEIGHT_INCHES[weight_key] * hook_factor
    sts_per_in = 1.0 / stitch_width_in
    rows_per_in = 1.0 / stitch_height_in

    # Resolve target max diameter in inches & max equator stitches
    if max_diameter_inches is not None:
        width_in = max_diameter_inches
        max_sts = max(12, 6 * round((math.pi * width_in * sts_per_in) / 6))
    elif max_diameter_cm is not None:
        width_in = max_diameter_cm / CM_PER_INCH
        max_sts = max(12, 6 * round((math.pi * width_in * sts_per_in) / 6))
    else:
        if max_diameter_stitches <= 6:
            raise HTTPException(status_code=400, detail="max_diameter_stitches must be greater than 6.")
        max_sts = max(12, 6 * round(max_diameter_stitches / 6))
        width_in = (max_sts * stitch_width_in) / math.pi

    # Automatically calculate standard egg height from width
    height_in = width_in * STANDARD_EGG_ASPECT_RATIO
    total_rounds = max(8, round(height_in * rows_per_in))

    # Build asymmetric egg profile (narrow pointed top -> low equator -> rounded base)
    raw_profile = []
    for i in range(1, total_rounds + 1):
        t = (i - 0.5) / total_rounds
        base_ellipse = math.sqrt(max(0.0, 1.0 - (2.0 * t - 1.0) ** 2))
        skew = 1.0 - EGG_SKEW_FACTOR * (1.0 - 2.0 * t)
        raw_profile.append(base_ellipse * skew)

    peak_val = max(raw_profile)
    peak_idx = raw_profile.index(peak_val)

    counts = [0] * total_rounds
    counts[0] = 6
    counts[-1] = 6

    # Top half: pointed crown increasing down to equator
    for i in range(1, peak_idx + 1):
        ideal = round((raw_profile[i] / peak_val) * max_sts)
        max_allowed = min(counts[i - 1] + 6, counts[i - 1] * 2, max_sts)
        counts[i] = max(counts[i - 1], min(ideal, max_allowed))
    counts[peak_idx] = max_sts

    # Bottom half: rounded base increasing from magic ring up to equator
    for i in range(total_rounds - 2, peak_idx, -1):
        ideal = round((raw_profile[i] / peak_val) * max_sts)
        max_allowed = min(counts[i + 1] + 6, counts[i + 1] * 2, max_sts)
        counts[i] = max(counts[i + 1], min(ideal, max_allowed))

    # Identify the middle of the max-diameter equator rows for clean splitting
    equator_indices = [idx for idx, c in enumerate(counts) if c == max_sts]
    split_idx = equator_indices[len(equator_indices) // 2]

    is_split = shell_mode == ShellMode.split
    use_stuffing = (not is_split) and (stuffing == StuffingOption.yes)

    pattern = []
    total_stitches = 0

    if not is_split:
        # --- WHOLE SHELL (Single continuous piece, top to bottom) ---
        stuff_trigger_idx = max(1, len(counts) - 3)
        for idx, curr in enumerate(counts):
            rnd = idx + 1
            total_stitches += curr

            if rnd == 1:
                text = f"Rnd 1: Start {curr} sc in a magic ring. ({curr} sts)"
            else:
                prev = counts[idx - 1]
                diff = curr - prev
                if diff == 0:
                    text = f"Rnd {rnd}: sc in each st around. ({curr} sts)"
                elif diff > 0:
                    text = f"Rnd {rnd}: {_format_shaping_round(prev, diff, 'inc')}. ({curr} sts)"
                else:
                    text = f"Rnd {rnd}: {_format_shaping_round(prev, abs(diff), 'dec')}. ({curr} sts)"

            step_obj = {"round": rnd, "phase": "whole", "stitches_in_round": curr, "instruction": text}
            if use_stuffing and idx == stuff_trigger_idx:
                step_obj["stuffing_instruction"] = (
                    "Stuff the egg firmly with polyfill now, shaping the pointed top and rounded base before closing."
                )
            pattern.append(step_obj)

        pattern.append({
            "round": len(counts) + 1,
            "phase": "finish",
            "stitches_in_round": 0,
            "instruction": "Fasten off, leaving a 6-inch tail. Weave tail through front loops of the remaining 6 stitches and pull tight to close."
        })
        total_rounds_out = len(counts)
    else:
        # --- SPLIT IN HALF (Two separate pieces meeting at the middle max-diameter row) ---
        top_counts = counts[: split_idx + 1]
        bottom_counts = list(reversed(counts[split_idx + 1 :]))
        # Ensure bottom half reaches max_sts cleanly if split fell at the very last equator row
        if not bottom_counts or bottom_counts[-1] < max_sts:
            bottom_counts.append(max_sts)

        # Part 1: Top Half (Pointed Crown -> Equator)
        for idx, curr in enumerate(top_counts):
            rnd = idx + 1
            total_stitches += curr
            if rnd == 1:
                text = f"[Top Half] Rnd 1: Start {curr} sc in a magic ring. ({curr} sts)"
            else:
                prev = top_counts[idx - 1]
                diff = curr - prev
                if diff == 0:
                    text = f"[Top Half] Rnd {rnd}: sc in each st around. ({curr} sts)"
                else:
                    text = f"[Top Half] Rnd {rnd}: {_format_shaping_round(prev, diff, 'inc')}. ({curr} sts)"
            pattern.append({"round": rnd, "phase": "top_half", "stitches_in_round": curr, "instruction": text})

        pattern.append({
            "round": len(top_counts) + 1,
            "phase": "top_half_finish",
            "stitches_in_round": 0,
            "instruction": "[Top Half] Fasten off with an invisible join and weave in the end."
        })

        # Part 2: Bottom Half (Rounded Base -> Equator)
        for idx, curr in enumerate(bottom_counts):
            rnd = idx + 1
            total_stitches += curr
            if rnd == 1:
                text = f"[Bottom Half] Rnd 1: Start {curr} sc in a magic ring. ({curr} sts)"
            else:
                prev = bottom_counts[idx - 1]
                diff = curr - prev
                if diff == 0:
                    text = f"[Bottom Half] Rnd {rnd}: sc in each st around. ({curr} sts)"
                else:
                    text = f"[Bottom Half] Rnd {rnd}: {_format_shaping_round(prev, diff, 'inc')}. ({curr} sts)"
            pattern.append({"round": rnd, "phase": "bottom_half", "stitches_in_round": curr, "instruction": text})

        pattern.append({
            "round": len(bottom_counts) + 1,
            "phase": "bottom_half_finish",
            "stitches_in_round": 0,
            "instruction": (
                f"[Bottom Half] Fasten off, leaving a long tail if sewing the two halves together around the {max_sts}-stitch equator "
                f"(or weave in ends to leave as two open egg halves)."
            )
        })
        total_rounds_out = len(top_counts) + len(bottom_counts)

    # Calculate finished dimensions, yarn yardage, and stuffing metrics
    actual_width_in = round(max_sts / (math.pi * sts_per_in), 2)
    actual_height_in = round(total_rounds_out / rows_per_in, 2)

    hook_adjusted_inches_per_st = YARN_INCHES_PER_STITCH[weight_key] * hook_factor
    estimated_yards = round((total_stitches * hook_adjusted_inches_per_st / 36.0) * 1.15, 1)
    estimated_meters = round(estimated_yards * 0.9144, 1)
    estimated_grams = round(estimated_yards * YARN_GRAMS_PER_YARD[weight_key], 1)
    estimated_oz = round(estimated_grams / 28.3495, 1)

    volume_cubic_in = (4.0 / 3.0) * math.pi * ((actual_width_in / 2.0) ** 2) * (actual_height_in / 2.0)
    polyfill_oz = round(volume_cubic_in * 0.12, 1) if use_stuffing else 0.0
    formatted_hook_label = get_hook_label(hook_size_mm)

    return {
        "shape": "egg",
        "supplies_you_need": {
            "estimated_yarn": f"{estimated_yards} yards ({estimated_meters} meters)",
            "hook": formatted_hook_label,
            "stuffing_volume": (
                f"{polyfill_oz} oz of polyfill stuffing"
                if use_stuffing
                else ("N/A (Split in half)" if is_split else "None (Unstuffed)")
            ),
        },
        "parameters": {
            "yarn_weight": yarn_weight.value,
            "hook_label": formatted_hook_label,
            "hook_size_mm": hook_size_mm,
            "shell_mode": shell_mode.value,
            "stuffing": stuffing.value if not is_split else "no",
            "max_diameter_stitches": max_sts,
            "max_diameter_inches": max_diameter_inches,
            "max_diameter_cm": max_diameter_cm,
        },
        "dimensions": {
            "diameter_inches": actual_width_in,
            "diameter_cm": round(actual_width_in * CM_PER_INCH, 1),
            "height_inches": actual_height_in,
            "height_cm": round(actual_height_in * CM_PER_INCH, 1),
            "volume_cubic_inches": round(volume_cubic_in, 2),
            "total_stitches_worked": total_stitches,
            "estimated_yarn_yards": estimated_yards,
            "estimated_yarn_meters": estimated_meters,
            "estimated_weight_grams": estimated_grams,
            "estimated_weight_oz": estimated_oz,
            "polyfill_stuffing_oz": polyfill_oz,
        },
        "total_rounds": total_rounds_out,
        "pattern": pattern,
    }


def _format_shaping_round(prev_sts: int, changes: int, mode: Literal["inc", "dec"]) -> str:
    consumed = 1 if mode == "inc" else 2
    plain_sts = prev_sts - (changes * consumed)

    if plain_sts <= 0:
        return f"[{mode}] x {changes}"

    base_sc = plain_sts // changes
    extra_sc = plain_sts % changes

    if extra_sc == 0:
        return (
            f"[sc, {mode}] x {changes}"
            if base_sc == 1
            else f"[sc in next {base_sc} sts, {mode}] x {changes}"
        )

    parts = []
    acc = 0
    for _ in range(changes):
        acc += extra_sc
        sc_count = base_sc
        if acc >= changes:
            sc_count += 1
            acc -= changes
        step = (
            f"sc in next {sc_count} sts, {mode}"
            if sc_count > 1
            else (f"sc, {mode}" if sc_count == 1 else mode)
        )
        parts.append(step)

    compressed = []
    for p in parts:
        if compressed and compressed[-1][0] == p:
            compressed[-1][1] += 1
        else:
            compressed.append([p, 1])

    return ", ".join(
        f"[{seg}] x {cnt}" if cnt > 1 else seg for seg, cnt in compressed
    )

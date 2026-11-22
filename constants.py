from enum import Enum


class YarnWeight(str, Enum):
    fingering = "fingering"
    sport = "sport"
    dk = "dk"
    worsted = "worsted"
    bulky = "bulky"
    super_bulky = "super_bulky"


class StuffingOption(str, Enum):
    yes = "yes"
    no = "no"


CM_PER_INCH = 2.54

YARN_INCHES_PER_STITCH = {
    "fingering": 1.3,
    "sport": 1.8,
    "dk": 2.0,
    "worsted": 2.5,
    "bulky": 3.8,
    "super_bulky": 5.0,
}

YARN_STITCH_HEIGHT_INCHES = {
    "fingering": 0.15,
    "sport": 0.20,
    "dk": 0.22,
    "worsted": 0.28,
    "bulky": 0.40,
    "super_bulky": 0.55,
}

YARN_STITCH_WIDTH_INCHES = {
    "fingering": 0.18,
    "sport": 0.22,
    "dk": 0.25,
    "worsted": 0.30,
    "bulky": 0.42,
    "super_bulky": 0.58,
}

YARN_GRAMS_PER_YARD = {
    "fingering": 2.5,
    "sport": 3.0,
    "dk": 3.5,
    "worsted": 4.5,
    "bulky": 6.5,
    "super_bulky": 9.0,
}

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
    10.0: "N-14 (10.00mm)",
}


def get_hook_label(hook_mm: float) -> str:
    closest_size = min(HOOK_LABEL_MAP.keys(), key=lambda x: abs(x - hook_mm))
    if abs(closest_size - hook_mm) <= 0.15:
        return HOOK_LABEL_MAP[closest_size]
    return f"({hook_mm:.2f}mm)"

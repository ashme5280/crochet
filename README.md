# Amigurumi Pattern Generator

A full-stack web application that generates custom, round-by-round crochet instructions, stitch counts, physical dimensions, yarn yardage/weight estimates, and stuffing calculations for basic 3D amigurumi shapes.

## Supported Shapes

* **Sphere** (`sphere.html` / `generators/sphere.py`) — Generates proportional spheres sized by target diameter or maximum stitch count.
* **Cylinder** (`cylinder.html` / `generators/cylinder.py`) — Generates flat-bottomed tubes and cylinders with customizable diameter and height.
* **Cone** (`cone.html` / `generators/cone.py`) — Generates tapered cones with adjustable base diameter and height.
* **Oval** (`oval.html` / `generators/oval.py`) — Generates elongated capsules/ovals with customizable width and length.
* **Egg** (`egg.html` / `generators/egg.py`) — Generates asymmetric egg shapes with automatic height-to-diameter proportions, supporting both **Whole shell** and **Split in half** modes.

## Features

* **Flexible Sizing:** Calculate patterns based on target physical dimensions (**Inches** or **Centimeters**) or exact **Maximum Stitch Count**.
* **Yarn & Hook Calibration:** Supports **Fingering**, **Sport**, **DK**, **Worsted**, **Bulky**, and **Super Bulky** yarn weights alongside custom hook sizes (in mm).
* **Supply & Stuffing Estimates:** Automatically calculates total yarn required (in yards and meters), total round count, finished dimensions, and polyfill stuffing weight (in ounces/grams).
* **Interactive Pattern Checklists:** Generates round-by-round crochet instructions with checkable progress boxes, shaping tips, and **Print / Save as PDF** formatting.

## Project Structure

```text
.
├── constants.py          # Yarn weight gauges, hook conversions, and calculation constants
├── main.py               # FastAPI backend server and API endpoints
├── requirements.txt      # Python dependencies
├── frontend/             # Static web interface
│   ├── index.html        # Home / shape navigation
│   ├── sphere.html       # Sphere generator UI
│   ├── cylinder.html     # Cylinder generator UI
│   ├── cone.html         # Cone generator UI
│   ├── oval.html         # Oval generator UI
│   ├── egg.html          # Egg generator UI
│   ├── script.js         # Client-side form handling, API requests, and checklist rendering
│   └── styles.css        # Responsive layout and print-friendly styles
└── generators/           # Core amigurumi math and stitch-progression engines
    ├── sphere.py
    ├── cylinder.py
    ├── cone.py
    ├── oval.py
    └── egg.py

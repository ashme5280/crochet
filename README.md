# Crochet Amigurumi Pattern Generator API

A FastAPI-based backend service that automatically generates precise, round-by-round amigurumi crochet patterns for 3D shapes (spheres, cylinders, and cones) based on customizable dimensions, yarn weights, and hook sizes.

## Features

* **Multiple Shape Endpoints:** Generate patterns for [Spheres], [Cylinders], and [Cones].
* **Flexible Sizing Toggles:** Input target stitch counts, finished diameters (in inches or centimeters), or heights dynamically.
* **Precise Math & Metrics:** Automatically calculates finished dimensions, volume (cubic inches & cm), estimated yarn lengths (yards & meters), and yarn weights (grams & ounces).
* **Traditional Amigurumi Math:** Adheres to standard crochet rules (magic rings, all-increase start rounds, gradual taper distributions, and proper closing decrease caps).
* **Yarn Weight Categorization:** Built-in enum support for weights ranging from Fingering to Super Bulky.

## Frontend Web Interface

The project includes a lightweight, responsive single-page web interface (`frontend/index.html`) that allows users to interactively generate amigurumi patterns, switch between unit systems, and customize shapes in real-time.

### Features
* **Unit System Toggle:** Seamlessly switch between Imperial (**Inches**) and Metric (**Centimeters**).
* **Shape Selector:** Choose between **Sphere**, **Cylinder** (with open/closed ends configuration), and **Cone** (with Narrow, Medium, and Wide taper styles).
* **Dynamic Form Fields:** Form inputs update dynamically depending on the selected shape and measurement system.
* **Instant Metrics Card:** Displays total rounds, precise finished physical dimensions, and yarn estimates in both **yards** and **meters**.
* **Clean Instructions:** Renders a step-by-step, easy-to-read crochet pattern list.

### Running the Frontend Locally
1. Start your FastAPI backend server:
   ```bash
   uvicorn main:app --reload

amigurumi-generator/
│
├── frontend/
│   └── index.html          # Responsive single-page web UI (Unit toggles, shape selectors, live metrics & instructions)
│
├── generators/
│   ├── __init__.py         # Package initialization
│   ├── sphere.py           # Sphere geometry, yarn metrics, and pattern generator route
│   ├── cylinder.py         # Cylinder geometry, open/closed ends configuration, and route
│   └── cone.py             # Cone geometry, narrow/medium/wide taper styles, dynamic heights, and route
│
├── main.py                 # FastAPI application entry point wiring routers and CORS
├── requirements.txt        # Project dependencies (FastAPI, Uvicorn, etc.)
└── README.md               # Project documentation including API endpoints and frontend usage

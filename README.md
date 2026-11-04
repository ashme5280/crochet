# Crochet Amigurumi Pattern Generator API

A FastAPI-based backend service that automatically generates precise, round-by-round amigurumi crochet patterns for 3D shapes (spheres, cylinders, and cones) based on customizable dimensions, yarn weights, and hook sizes.

## Features

* **Multiple Shape Endpoints:** Generate patterns for [Spheres], [Cylinders], and [Cones].
* **Flexible Sizing Toggles:** Input target stitch counts, finished diameters (in inches or centimeters), or heights dynamically.
* **Precise Math & Metrics:** Automatically calculates finished dimensions, volume (cubic inches & cm), estimated yarn lengths (yards & meters), and yarn weights (grams & ounces).
* **Traditional Amigurumi Math:** Adheres to standard crochet rules (magic rings, all-increase start rounds, gradual taper distributions, and proper closing decrease caps).
* **Yarn Weight Categorization:** Built-in enum support for weights ranging from Fingering to Super Bulky.

## Project Structure

```text
├── generators/
│   ├── __init__.py
│   ├── sphere.py      # Sphere pattern & volumetric logic
│   ├── cylinder.py    # Cylinder pattern & height/tube logic
│   └── cone.py        # Cone pattern & smooth single-stitch taper logic
├── main.py            # FastAPI application entry point
└── requirements.txt   # Project dependencies

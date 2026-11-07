# Amigurumi Pattern Generator API & Application

A full-stack application designed to dynamically calculate and generate custom crochet amigurumi patterns, complete with precise stitch counts, yardage estimators, dimensions, and assembly instructions.

---

## Features

* **Multi-Shape Generation:** Automatically computes round-by-round crochet instructions for various amigurumi components (Spheres, Ovals, Cones, Cylinders, etc.).
* **Dynamic Sizing:** Supports custom inputs by length, width, height, or base stitch count/diameter across multiple yarn weights (Fingering to Super Bulky) and hook sizes.
* **Smart Adjustments:** 
  * Ovals mirror their expansion and decrease phases symmetrically back to the starting foundation count.
  * Open-cone shapes include specific final expansion calculations and specialized open-cone stuffing and attachment tail instructions.
* **Yarn & Material Estimators:** Calculates estimated yardage, meters, weight (grams/oz), and finished dimensions automatically.
* **FastAPI Backend:** Built with high-performance Python endpoints supporting clean query parameters and robust validation.
* **Interactive Frontend:** Built with React, Vite, and Tailwind CSS for real-time pattern customization and previewing.

---

## Project Structure

```text
amigurumi-generator/
│
├── frontend/                # React / Vite frontend application
│   ├── public/              # Static assets
│   ├── src/                 # Source code components and UI
│   │   ├── App.jsx          # Main application component
│   │   ├── main.jsx         # React DOM entry point
│   │   └── index.css        # Tailwind CSS styles
│   ├── index.html           # HTML template
│   ├── package.json         # Frontend dependencies and scripts
│   └── vite.config.js       # Vite configuration
│
├── generators/              # Shape pattern calculation modules
│   ├── __init__.py
│   ├── oval.py              # Oval component generator
│   ├── cone.py              # Open cone/tail generator
│   └── sphere.py            # Sphere component generator
│
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

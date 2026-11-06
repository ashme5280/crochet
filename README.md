# Amigurumi Pattern Generator

A full-stack application and API that generates precise, custom round-by-round crochet patterns, dimensions, and yarn estimates for amigurumi components.

---

## Features
* **Multi-Shape Support:** Generate custom patterns for **Spheres**, **Cylinders**, **Cones**, and **Ovals** (egg-shaped).
* **Dynamic Sizing:** Input your target dimensions in either **Imperial (inches)** or **Metric (centimeters)**.
* **Yarn & Hook Customization:** Select from various yarn weights (Fingering to Super Bulky) and hook sizes.
* **Smart Finishing Tips:** Built-in stuffing guidelines and finishing instructions ("Fasten off and weave in tail.") tailored to each component shape.

---

## Project Structure

```text
amigurumi-generator/
│
├── backend/
│   ├── main.py              # FastAPI application server & routing endpoints
│   ├── generator.py         # Core mathematical pattern generation logic for shapes
│   └── requirements.py      # Python backend dependencies
│
├── frontend/
│   └── index.html           # Interactive HTML/JS client interface
│
├── README.md                # Project documentation and setup guide
└── render.yaml              # Cloud hosting deployment configurations for Render

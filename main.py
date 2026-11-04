from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from generators import sphere, cylinder, cone

app = FastAPI(
    title="Amigurumi Component Generator API",
    description="Calculates row-by-row crochet instructions, physical dimensions, and exact yarn yardage.",
    version="2.0.0"
)

# Mount shape routers
app.include_router(sphere.router)
app.include_router(cylinder.router)
app.include_router(cone.router)

# Mount your frontend directory
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def read_index():
    return FileResponse("frontend/index.html")

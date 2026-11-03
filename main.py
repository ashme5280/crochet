from fastapi import FastAPI
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

@app.get("/")
def root():
    return {"message": "Welcome to the Amigurumi Generator API! Visit /docs to test all shapes."}

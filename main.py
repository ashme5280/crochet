from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from generators import sphere, cylinder, cone, oval

app = FastAPI(
    title="Amigurumi Component Generator API",
    description="Calculates row-by-row crochet instructions, physical dimensions, and exact yarn yardage.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount shape routers
app.include_router(sphere.router)
app.include_router(cylinder.router)
app.include_router(cone.router)
app.include_router(oval.router)

# 1. Serve sphere.html as the root home page
@app.get("/")
def read_root():
    return FileResponse("frontend/sphere.html")

# 2. Mount static files from the local frontend folder
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

"""
Adaptive Network Design and Optimization Framework
FastAPI Backend Application Entrypoint
Assignment 4: Design and Analysis of Algorithms (AI ML Leopards)
Faculty: Professor Geeta Tripathi, Professor of Practice
"""

import sys
import os

# Ensure backend root is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import init_db
from .routers.structures import sync_initial_structures
from .routers import (
    network,
    algorithms,
    structures,
    optimization,
    experiments,
    dashboard
)
from .models.schemas import ApiResponse

app = FastAPI(
    title="Adaptive Network Design and Optimization Framework",
    description=(
        "Comprehensive DAA Course Project backend integrating Graph Algorithms (Prim, Kruskal, Floyd-Warshall), "
        "Advanced Data Structures (B-Tree, Red-Black Tree, Binomial Heap, Fibonacci Heap), "
        "Combinatorial Optimization (Knapsack, TSP), and an Explainable Decision Engine."
    ),
    version="1.0.0"
)

# CORS configuration for frontend dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initializes SQLite database and warms in-memory tree & heap structures."""
    init_db()
    sync_initial_structures()


@app.get("/api/health", response_model=ApiResponse, tags=["Health"])
def health_check():
    """API Health Check Endpoint."""
    return ApiResponse(
        success=True,
        data={
            "status": "healthy",
            "app": "Adaptive Network Framework",
            "version": "1.0.0",
            "course": "Design and Analysis of Algorithms",
            "faculty": "Prof. Geeta Tripathi"
        },
        message="Backend operational and healthy."
    )


# Register Module Routers
app.include_router(dashboard.router)
app.include_router(network.router)
app.include_router(algorithms.router)
app.include_router(structures.router)
app.include_router(optimization.router)
app.include_router(experiments.router)


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": str(exc),
            "message": "An internal error occurred during algorithm execution."
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

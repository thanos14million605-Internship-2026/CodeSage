from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analysis import router as analysis_router
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
import os

app = FastAPI(
    title="CodeSage ML API",
    description="AI-powered code analysis and bug-risk prediction system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://codesage-h1pb.onrender.com", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis_router, prefix="/api", tags=["analysis"])

@app.get("/")
async def root():
    return {"message": "CodeSage ML API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "CodeSage ML API"}

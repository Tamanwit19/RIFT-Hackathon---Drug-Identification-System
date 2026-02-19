from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI(title="PharmaGenie PGx API")

# IMPORTANT: Allow your React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "PharmaGenie API is Online"}
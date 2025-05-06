from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .rotas import auth, posts
from .modelo.database import init_db

app = FastAPI(title="Social Network API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/api", tags=["posts"])

@app.get("/")
async def root():
    return {"message": "Welcome to Social Network API"} 
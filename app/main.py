from fastapi import FastAPI
from .routers import item, user  # Import routers from subdirectories

app = FastAPI()

# Include routers for different parts of your application
app.include_router(item.router, prefix="/items", tags=["items"])
# app.include_router(user.router, prefix="/users", tags=["users"])

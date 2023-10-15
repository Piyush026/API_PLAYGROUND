from fastapi import FastAPI
from app.items import routes

app = FastAPI()

# Include routers for different parts of your application
app.include_router(routes.router, prefix="/items", tags=["items"])
# app.include_router(user.router, prefix="/users", tags=["users"])

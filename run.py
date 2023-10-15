from fastapi import FastAPI
import logging

from app.items import routes as items_routes
from app.users_app import routes as users_routes

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(items_routes.router, prefix="/items", tags=["Items"])
app.include_router(users_routes.router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

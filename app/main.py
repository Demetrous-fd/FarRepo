from fastapi import FastAPI

from app.routes import routes



def create_app() -> FastAPI:
    app = FastAPI()
    for route in routes:
        app.include_router(route)
    
    return app


app = create_app()

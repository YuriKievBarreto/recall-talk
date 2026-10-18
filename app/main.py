from fastapi import FastAPI
from app.api.routes import auth_router

app = FastAPI()
app.include_router(auth_router.router, prefix="/auth")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
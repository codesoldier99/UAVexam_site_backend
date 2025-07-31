from fastapi import FastAPI
from src.routers import users
from src.institutions.router import router as institutions_router
from src.auth.router import router as auth_router
from src.auth.social import router as social_router

app = FastAPI(title="Exam Site Backend API")

app.include_router(users.router)
app.include_router(institutions_router)
app.include_router(auth_router)
app.include_router(social_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Exam Site Backend API"}

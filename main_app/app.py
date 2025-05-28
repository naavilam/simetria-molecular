from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .main_routes import router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conecta as rotas
app.include_router(router)
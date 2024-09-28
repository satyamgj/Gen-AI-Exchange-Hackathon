# app/main.py

from fastapi import FastAPI
from app.api.endpoints import chatApi
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the process_file router
app.include_router(chatApi.router, prefix="/api/v1", tags=["Chat application"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG FastAPI service!"}

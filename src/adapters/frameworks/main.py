from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import audios

app = FastAPI(openapi_url="/api/docs/openapi.json",
              docs_url="/api/docs",
              redoc_url="/api/redoc",
              title="Whisper API",
              description="Whisper API for TCK")

origins = [
    "http://127.0.0.1",
    "http://localhost:63342",
    "https://whisper-demo.tck.link"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(audios.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

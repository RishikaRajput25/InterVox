# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.documents import router as documents_router
# app = FastAPI(
#     title="AI Research Assistant API",
#     version="0.1.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.include_router(documents_router)

# @app.get("/")
# async def root():
#     return {
#         "message": "AI Research Assistant API is running"
#     }


# @app.get("/health")
# async def health_check():
#     return {
#         "status": "ok"
#     }


# def dev():
#     import uvicorn

#     uvicorn.run(
#         "app.main:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True,
#     )


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.documents import router as documents_router
from app.api.voice import router as voice_router


app = FastAPI(
    title="AI Research Assistant API",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(documents_router)
app.include_router(voice_router)


@app.get("/")
async def root():
    return {
        "message": "AI Research Assistant API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "ok"
    }


def dev():
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.interfaces.api.routes import router as api_router
from app.infrastructure.settings import settings
from app.infrastructure.logging import setup_logging
from app.infrastructure.rate_limit import RateLimitMiddleware


def create_app() -> FastAPI:
    setup_logging()
    
    app = FastAPI(title="ProviderSyncAI", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(RateLimitMiddleware)

    app.include_router(api_router, prefix=settings.api_prefix)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



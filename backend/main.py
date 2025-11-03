from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.interfaces.api.routes import router as api_router
from app.interfaces.api.workflow_routes import router as workflow_router
from app.interfaces.api.metrics_routes import router as metrics_router
from app.infrastructure.settings import settings
from app.infrastructure.logging import setup_logging
from app.infrastructure.rate_limit import RateLimitMiddleware
from app.infrastructure.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


def create_app() -> FastAPI:
    setup_logging()
    
    app = FastAPI(title="ProviderSyncAI", version="0.1.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(RateLimitMiddleware)

    app.include_router(api_router, prefix=settings.api_prefix)
    app.include_router(workflow_router, prefix=settings.api_prefix)
    app.include_router(metrics_router, prefix=settings.api_prefix)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



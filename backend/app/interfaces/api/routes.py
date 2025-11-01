from fastapi import APIRouter, HTTPException
from ...domain.entities import SearchQuery
from .schemas import ProviderSearchRequest, ProviderSearchResponse, ProviderDTO
from ...application.use_cases.search_providers import execute
from ...infrastructure.logging import get_logger


router = APIRouter()
logger = get_logger(__name__)


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/search/providers", response_model=ProviderSearchResponse)
async def search_providers(payload: ProviderSearchRequest) -> ProviderSearchResponse:
    try:
        query = SearchQuery(**payload.model_dump())
        result = await execute(query)
        providers = [
            ProviderDTO(**p.model_dump())
            for p in result.providers
        ]
        return ProviderSearchResponse(providers=providers)
    except ValueError as e:
        logger.warning("validation_error", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("search_error", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/agents/run")
async def run_agent(request: dict):
    """Optional endpoint for direct agent interaction (debugging)."""
    try:
        prompt = request.get("prompt", "")
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        from ...agents.agent import build_agent
        agent = build_agent()
        result = await agent.run(prompt)
        return {"result": str(result)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("agent_error", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Agent execution failed")



"""Quality metrics API routes."""
from fastapi import APIRouter
from typing import Optional
from ...infrastructure.services.quality_metrics_service import QualityMetricsService
from ...infrastructure.logging import get_logger


router = APIRouter()
logger = get_logger(__name__)


@router.get("/metrics")
async def get_metrics(metric_name: Optional[str] = None, days: int = 30) -> dict:
    """Get quality metrics."""
    try:
        service = QualityMetricsService()
        metrics = await service.get_metrics(metric_name=metric_name, days=days)
        
        return {
            "metrics": [
                {
                    "metric_name": m.metric_name,
                    "value": m.value,
                    "threshold": m.threshold,
                    "trend": m.trend,
                    "measured_at": m.measured_at.isoformat(),
                }
                for m in metrics
            ]
        }
    except Exception as e:
        logger.error("metrics_fetch_failed", error=str(e), exc_info=True)
        raise


@router.get("/metrics/directory-quality")
async def get_directory_quality() -> dict:
    """Get overall directory quality score."""
    try:
        service = QualityMetricsService()
        score = await service.calculate_directory_quality_score()
        
        return {
            "directory_quality_score": score,
            "threshold": 0.8,
            "status": "meeting_threshold" if score >= 0.8 else "below_threshold",
        }
    except Exception as e:
        logger.error("directory_quality_failed", error=str(e), exc_info=True)
        raise


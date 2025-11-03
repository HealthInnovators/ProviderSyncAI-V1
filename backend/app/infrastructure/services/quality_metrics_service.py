"""Quality metrics tracking service."""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from ...domain.enriched_entities import QualityMetric
from ...infrastructure.database import get_db
from ...infrastructure.database.models import QualityMetricModel
from sqlalchemy import select, func
from ...infrastructure.logging import get_logger


logger = get_logger(__name__)


class QualityMetricsService:
    """Service for tracking and analyzing quality metrics."""
    
    async def record_metric(self, metric_name: str, value: float, 
                           threshold: Optional[float] = None,
                           metadata: Optional[dict] = None):
        """Record a quality metric."""
        db = get_db()
        async with db.get_session() as session:
            metric = QualityMetricModel(
                metric_name=metric_name,
                value=value,
                threshold=threshold,
                trend=None,  # Would be calculated on read
                metadata_json=metadata or {},
            )
            session.add(metric)
            await session.flush()
    
    async def get_metrics(self, metric_name: Optional[str] = None,
                         days: int = 30) -> List[QualityMetric]:
        """Get quality metrics."""
        db = get_db()
        async with db.get_session() as session:
            since = datetime.utcnow() - timedelta(days=days)
            
            query = select(QualityMetricModel).where(
                QualityMetricModel.measured_at >= since
            )
            
            if metric_name:
                query = query.where(QualityMetricModel.metric_name == metric_name)
            
            query = query.order_by(QualityMetricModel.measured_at.desc())
            
            result = await session.execute(query)
            metrics = result.scalars().all()
            
            # Calculate trends
            metrics_list = []
            for m in metrics:
                trend = await self._calculate_trend(session, m.metric_name, m.measured_at)
                metrics_list.append(QualityMetric(
                    metric_name=m.metric_name,
                    value=m.value,
                    threshold=m.threshold,
                    trend=trend,
                    measured_at=m.measured_at,
                ))
            
            return metrics_list
    
    async def _calculate_trend(self, session, metric_name: str, current_time: datetime) -> str:
        """Calculate trend for a metric."""
        # Compare with previous period
        prev_start = current_time - timedelta(days=7)
        prev_end = current_time - timedelta(days=1)
        
        current_start = current_time - timedelta(days=1)
        
        # Get previous average
        prev_query = select(func.avg(QualityMetricModel.value)).where(
            QualityMetricModel.metric_name == metric_name,
            QualityMetricModel.measured_at >= prev_start,
            QualityMetricModel.measured_at < prev_end,
        )
        prev_result = await session.execute(prev_query)
        prev_avg = prev_result.scalar() or 0.0
        
        # Get current average
        current_query = select(func.avg(QualityMetricModel.value)).where(
            QualityMetricModel.metric_name == metric_name,
            QualityMetricModel.measured_at >= current_start,
            QualityMetricModel.measured_at < current_time,
        )
        current_result = await session.execute(current_query)
        current_avg = current_result.scalar() or 0.0
        
        # Determine trend
        if abs(current_avg - prev_avg) < 0.05:
            return "stable"
        elif current_avg > prev_avg:
            return "improving"
        else:
            return "declining"
    
    async def calculate_directory_quality_score(self) -> float:
        """Calculate overall directory quality score."""
        db = get_db()
        async with db.get_session() as session:
            from ...infrastructure.database.models import ProviderModel
            
            # Get average confidence across all providers
            query = select(func.avg(ProviderModel.overall_confidence))
            result = await session.execute(query)
            avg_confidence = result.scalar() or 0.0
            
            # Record metric
            await self.record_metric("directory_quality_score", avg_confidence, threshold=0.8)
            
            return round(avg_confidence, 2)


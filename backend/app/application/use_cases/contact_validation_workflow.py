"""Contact validation workflow use case."""
from typing import List
from ...domain.enriched_entities import EnrichedProvider, ValidationBatch
from ...infrastructure.services.orchestrator import AgentOrchestrator
from ...infrastructure.repositories.provider_repository import ProviderRepository
from ...infrastructure.database import get_db
from ...infrastructure.services.email_service import EmailService
from ...infrastructure.services.confidence_scoring import ConfidenceScoringService
from ...infrastructure.logging import get_logger
from datetime import datetime
import uuid


logger = get_logger(__name__)


class ContactValidationWorkflow:
    """Workflow for automated contact information validation."""
    
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
        self.email_service = EmailService()
        self.confidence_scoring = ConfidenceScoringService()
    
    async def execute_batch(self, providers: List[EnrichedProvider]) -> ValidationBatch:
        """Execute batch contact validation."""
        batch_id = str(uuid.uuid4())
        logger.info("batch_validation_start", batch_id=batch_id, count=len(providers))
        
        batch = ValidationBatch(
            batch_id=batch_id,
            total_providers=len(providers),
            started_at=datetime.utcnow(),
            status="processing",
        )
        
        # Validate providers
        validated_providers = await self.orchestrator.batch_validate_providers(providers)
        
        # Update batch stats
        batch.processed_count = len(validated_providers)
        batch.validated_count = sum(1 for p in validated_providers if p.validation_status.value == "validated")
        batch.discrepancy_count = sum(1 for p in validated_providers if p.discrepancies)
        batch.requires_review_count = sum(1 for p in validated_providers if p.requires_manual_review)
        batch.providers = validated_providers
        batch.completed_at = datetime.utcnow()
        batch.status = "completed"
        
        # Save to database
        db = get_db()
        async with db.get_session() as session:
            repo = ProviderRepository(session)
            
            for provider in validated_providers:
                # Save or update provider
                existing = await repo.get_by_npi(provider.npi)
                if existing:
                    await repo.update(provider)
                else:
                    await repo.create(provider)
        
        logger.info("batch_validation_complete", batch_id=batch_id, validated=batch.validated_count)
        return batch


"""Credential verification workflow use case."""
from typing import List
from ...domain.enriched_entities import EnrichedProvider
from ...infrastructure.services.orchestrator import AgentOrchestrator
from ...infrastructure.repositories.provider_repository import ProviderRepository
from ...infrastructure.database import get_db
from ...infrastructure.logging import get_logger


logger = get_logger(__name__)


class CredentialVerificationWorkflow:
    """Workflow for new provider credential verification."""
    
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
    
    async def verify_provider_credentials(self, provider: EnrichedProvider) -> EnrichedProvider:
        """Verify provider credentials."""
        logger.info("verifying_credentials", npi=provider.npi)
        
        # Use information enrichment agent primarily
        provider = await self.orchestrator.information_enrichment_agent.enrich_provider(provider)
        
        # Quality assurance
        provider = await self.orchestrator.quality_assurance_agent.assess_quality(provider)
        
        # Save to database
        db = get_db()
        async with db.get_session() as session:
            repo = ProviderRepository(session)
            existing = await repo.get_by_npi(provider.npi)
            if existing:
                await repo.update(provider)
            else:
                await repo.create(provider)
        
        logger.info("credentials_verified", npi=provider.npi)
        return provider


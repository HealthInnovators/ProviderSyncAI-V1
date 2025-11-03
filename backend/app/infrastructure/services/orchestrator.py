"""Agent orchestration service."""
from typing import List
from ...domain.enriched_entities import EnrichedProvider
from ...infrastructure.models.grok_model import GrokModel
from ...agents.specialized.data_validation_agent import DataValidationAgent
from ...agents.specialized.information_enrichment_agent import InformationEnrichmentAgent
from ...agents.specialized.quality_assurance_agent import QualityAssuranceAgent
from ...agents.specialized.directory_management_agent import DirectoryManagementAgent
from ...infrastructure.logging import get_logger


logger = get_logger(__name__)


class AgentOrchestrator:
    """Orchestrates multiple agents for provider validation workflows."""
    
    def __init__(self, model: GrokModel):
        self.data_validation_agent = DataValidationAgent(model)
        self.information_enrichment_agent = InformationEnrichmentAgent(model)
        self.quality_assurance_agent = QualityAssuranceAgent(model)
        self.directory_management_agent = DirectoryManagementAgent(model)
    
    async def validate_provider_workflow(self, provider: EnrichedProvider) -> EnrichedProvider:
        """Complete validation workflow for a provider."""
        logger.info("starting_validation_workflow", npi=provider.npi)
        
        # Step 1: Data Validation
        provider = await self.data_validation_agent.validate_provider_contact(provider)
        
        # Step 2: Information Enrichment
        provider = await self.information_enrichment_agent.enrich_provider(provider)
        
        # Step 3: Quality Assurance
        provider = await self.quality_assurance_agent.assess_quality(provider)
        
        logger.info("validation_workflow_complete", npi=provider.npi, status=provider.validation_status.value)
        return provider
    
    async def batch_validate_providers(self, providers: List[EnrichedProvider]) -> List[EnrichedProvider]:
        """Batch validate multiple providers."""
        logger.info("batch_validation_start", count=len(providers))
        
        results = []
        for provider in providers:
            try:
                validated = await self.validate_provider_workflow(provider)
                results.append(validated)
            except Exception as e:
                logger.error("provider_validation_failed", npi=provider.npi, error=str(e))
                provider.requires_manual_review = True
                provider.review_priority = 10
                results.append(provider)
        
        logger.info("batch_validation_complete", total=len(providers), validated=len(results))
        return results


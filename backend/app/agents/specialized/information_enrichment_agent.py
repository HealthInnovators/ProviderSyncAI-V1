"""Information Enrichment Agent for adding provider data."""
from typing import List
from smolagents import CodeAgent, Tool
from ...domain.enriched_entities import EnrichedProvider
from ...infrastructure.models.grok_model import GrokModel
from ..tools.nppes_tool import NppesTool
from ..tools.web_search_tool import WebSearchTool
from ..tools.state_licensing_tool import StateLicensingTool
from ...infrastructure.logging import get_logger


logger = get_logger(__name__)


class InformationEnrichmentAgent:
    """Agent for enriching provider information from multiple sources."""
    
    def __init__(self, model: GrokModel):
        tools: List[Tool] = [
            NppesTool(),
            WebSearchTool(),
            StateLicensingTool(),
        ]
        self.agent = CodeAgent(tools=tools, model=model, name="information_enrichment_agent")
    
    async def enrich_provider(self, provider: EnrichedProvider) -> EnrichedProvider:
        """Enrich provider with additional information."""
        logger.info("enriching_provider", npi=provider.npi)
        
        prompt = f"""Enrich provider information for {provider.first_name} {provider.last_name} (NPI: {provider.npi}).

Current information:
- Name: {provider.first_name} {provider.last_name}
- Location: {provider.city}, {provider.state}
- Specialty: {provider.taxonomy}

Tasks:
1. Use nppes_search to get detailed provider information
2. Use web_search to find provider's education, board certifications, and specialties
3. Use state_license_lookup to get license information if available
4. Identify network affiliations and facility relationships
5. Find services offered by the provider

Return enriched information including:
- Education history
- Board certifications
- Additional specialties
- Network affiliations
- Services offered
"""
        
        try:
            result = await self.agent.run(prompt)
            # Process and update provider with enriched data
            # This would parse the agent result and update provider fields
            logger.info("provider_enriched", npi=provider.npi)
            return provider
        except Exception as e:
            logger.error("enrichment_failed", npi=provider.npi, error=str(e))
            return provider


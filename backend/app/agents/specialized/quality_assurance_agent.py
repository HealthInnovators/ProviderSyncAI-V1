"""Quality Assurance Agent for discrepancy detection."""
from typing import List
from smolagents import CodeAgent, Tool
from ...domain.enriched_entities import EnrichedProvider, ValidationStatus
from ...infrastructure.models.grok_model import GrokModel
from ..tools.nppes_tool import NppesTool
from ...infrastructure.logging import get_logger


logger = get_logger(__name__)


class QualityAssuranceAgent:
    """Agent for quality assurance and discrepancy detection."""
    
    def __init__(self, model: GrokModel):
        tools: List[Tool] = [
            NppesTool(),
        ]
        self.agent = CodeAgent(tools=tools, model=model, name="quality_assurance_agent")
    
    async def assess_quality(self, provider: EnrichedProvider) -> EnrichedProvider:
        """Assess provider data quality and detect discrepancies."""
        logger.info("assessing_quality", npi=provider.npi)
        
        prompt = f"""Assess data quality for provider {provider.first_name} {provider.last_name} (NPI: {provider.npi}).

Provider data:
- Contact: {provider.phone}, {provider.email}
- Address: {provider.address_line1}, {provider.city}, {provider.state}
- Confidence scores: Overall={provider.overall_confidence}, Phone={provider.phone_confidence}, Email={provider.email_confidence}, Address={provider.address_confidence}

Tasks:
1. Use nppes_search to cross-reference with official registry
2. Identify any inconsistencies or discrepancies
3. Flag suspicious or potentially fraudulent information
4. Calculate quality metrics
5. Determine if manual review is required
6. Assign review priority (1-10, higher = more urgent)

Return assessment with:
- Discrepancies found
- Quality score
- Review priority
- Flags for manual review
"""
        
        try:
            result = await self.agent.run(prompt)
            
            # Process assessment results
            # Check for discrepancies
            if provider.overall_confidence < 0.6:
                provider.requires_manual_review = True
                provider.review_priority = 8
                provider.validation_status = ValidationStatus.FLAGGED
                provider.discrepancies.append("Low confidence score detected")
            
            # Check for data inconsistencies
            if provider.phone_confidence < 0.5 or provider.email_confidence < 0.5:
                provider.discrepancies.append("Contact information has low confidence")
                provider.requires_manual_review = True
                if provider.review_priority < 7:
                    provider.review_priority = 7
            
            logger.info("quality_assessed", npi=provider.npi, priority=provider.review_priority)
            return provider
        except Exception as e:
            logger.error("quality_assessment_failed", npi=provider.npi, error=str(e))
            return provider


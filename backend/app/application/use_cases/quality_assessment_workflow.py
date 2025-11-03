"""Quality assessment workflow use case."""
from typing import List
from ...domain.enriched_entities import ValidationReport, EnrichedProvider
from ...infrastructure.services.orchestrator import AgentOrchestrator
from ...infrastructure.repositories.provider_repository import ProviderRepository
from ...infrastructure.database import get_db
from ...infrastructure.services.confidence_scoring import ConfidenceScoringService
from ...infrastructure.logging import get_logger
from datetime import datetime
import uuid


logger = get_logger(__name__)


class QualityAssessmentWorkflow:
    """Workflow for quality assessment of provider directory."""
    
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
        self.confidence_scoring = ConfidenceScoringService()
    
    async def assess_directory_quality(self, provider_ids: List[str]) -> ValidationReport:
        """Assess quality of provider directory."""
        logger.info("quality_assessment_start", provider_count=len(provider_ids))
        
        db = get_db()
        providers = []
        
        async with db.get_session() as session:
            repo = ProviderRepository(session)
            
            for npi in provider_ids:
                provider_model = await repo.get_by_npi(npi)
                if provider_model:
                    # Convert to EnrichedProvider
                    provider = self._model_to_enriched(provider_model)
                    # Re-assess quality
                    provider = await self.orchestrator.quality_assurance_agent.assess_quality(provider)
                    providers.append(provider)
        
        # Generate report
        batch_id = str(uuid.uuid4())
        from ...domain.enriched_entities import ValidationBatch
        batch = ValidationBatch(
            batch_id=batch_id,
            total_providers=len(providers),
            processed_count=len(providers),
            validated_count=sum(1 for p in providers if p.validation_status.value == "validated"),
            discrepancy_count=sum(1 for p in providers if p.discrepancies),
            requires_review_count=sum(1 for p in providers if p.requires_manual_review),
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            status="completed",
            providers=providers,
        )
        
        report = await self.orchestrator.directory_management_agent.generate_report(batch, providers)
        
        logger.info("quality_assessment_complete", report_id=report.report_id)
        return report
    
    def _model_to_enriched(self, model) -> EnrichedProvider:
        """Convert database model to EnrichedProvider."""
        from ...domain.enriched_entities import (
            EnrichedProvider, ProviderCredential, ProviderLicense, 
            ValidationStatus, DataElementConfidence, DataSource
        )
        
        # Parse credentials
        credentials = None
        if model.credentials_json:
            cred_data = model.credentials_json
            credentials = ProviderCredential(
                education=cred_data.get("education", []),
                board_certifications=cred_data.get("board_certifications", []),
                specialties=cred_data.get("specialties", []),
                years_of_experience=cred_data.get("years_of_experience"),
            )
        
        # Parse licenses
        licenses = []
        if model.licenses_json:
            for lic_data in model.licenses_json:
                licenses.append(ProviderLicense(**lic_data))
        
        # Parse data element confidences
        element_confidences = []
        if model.data_element_confidences_json:
            for de_data in model.data_element_confidences_json:
                element_confidences.append(DataElementConfidence(**de_data))
        
        return EnrichedProvider(
            npi=model.npi,
            enumeration_type=model.enumeration_type,
            first_name=model.first_name,
            last_name=model.last_name,
            organization_name=model.organization_name,
            phone=model.phone,
            phone_confidence=model.phone_confidence,
            email=model.email,
            email_confidence=model.email_confidence,
            address_line1=model.address_line1,
            address_line2=model.address_line2,
            city=model.city,
            state=model.state,
            postal_code=model.postal_code,
            address_confidence=model.address_confidence,
            taxonomy=model.taxonomy,
            credentials=credentials,
            licenses=licenses,
            network_affiliations=model.network_affiliations or [],
            facility_affiliations=model.facility_affiliations or [],
            services_offered=model.services_offered or [],
            appointment_availability=model.appointment_availability,
            website=model.website,
            google_places_id=model.google_places_id,
            validation_status=ValidationStatus(model.validation_status),
            overall_confidence=model.overall_confidence,
            data_element_confidences=element_confidences,
            last_validated=model.last_validated,
            validation_notes=model.validation_notes_json or [],
            requires_manual_review=model.requires_manual_review,
            review_priority=model.review_priority,
            discrepancies=model.discrepancies_json or [],
        )


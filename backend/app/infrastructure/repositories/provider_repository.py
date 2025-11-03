"""Provider repository for data access."""
from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.enriched_entities import EnrichedProvider, ValidationStatus
from ..database.models import ProviderModel, ValidationRecordModel
from datetime import datetime


class ProviderRepository:
    """Repository for provider data access."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, provider: EnrichedProvider) -> ProviderModel:
        """Create a new provider."""
        db_provider = ProviderModel(
            npi=provider.npi,
            enumeration_type=provider.enumeration_type,
            first_name=provider.first_name,
            last_name=provider.last_name,
            organization_name=provider.organization_name,
            phone=provider.phone,
            phone_confidence=provider.phone_confidence,
            email=provider.email,
            email_confidence=provider.email_confidence,
            address_line1=provider.address_line1,
            address_line2=provider.address_line2,
            city=provider.city,
            state=provider.state,
            postal_code=provider.postal_code,
            address_confidence=provider.address_confidence,
            taxonomy=provider.taxonomy,
            credentials_json=provider.credentials.model_dump() if provider.credentials else None,
            licenses_json=[lic.model_dump() for lic in provider.licenses] if provider.licenses else [],
            network_affiliations=provider.network_affiliations,
            facility_affiliations=provider.facility_affiliations,
            services_offered=provider.services_offered,
            appointment_availability=provider.appointment_availability,
            website=provider.website,
            google_places_id=provider.google_places_id,
            validation_status=provider.validation_status.value,
            overall_confidence=provider.overall_confidence,
            data_element_confidences_json=[de.model_dump() for de in provider.data_element_confidences],
            last_validated=provider.last_validated,
            validation_notes_json=provider.validation_notes,
            requires_manual_review=provider.requires_manual_review,
            review_priority=provider.review_priority,
            discrepancies_json=provider.discrepancies,
        )
        self.session.add(db_provider)
        await self.session.flush()
        return db_provider
    
    async def get_by_npi(self, npi: str) -> Optional[ProviderModel]:
        """Get provider by NPI."""
        result = await self.session.execute(
            select(ProviderModel).where(ProviderModel.npi == npi)
        )
        return result.scalar_one_or_none()
    
    async def update(self, provider: EnrichedProvider) -> Optional[ProviderModel]:
        """Update existing provider."""
        db_provider = await self.get_by_npi(provider.npi)
        if not db_provider:
            return None
        
        # Update all fields
        db_provider.first_name = provider.first_name
        db_provider.last_name = provider.last_name
        db_provider.organization_name = provider.organization_name
        db_provider.phone = provider.phone
        db_provider.phone_confidence = provider.phone_confidence
        db_provider.email = provider.email
        db_provider.email_confidence = provider.email_confidence
        db_provider.address_line1 = provider.address_line1
        db_provider.address_line2 = provider.address_line2
        db_provider.city = provider.city
        db_provider.state = provider.state
        db_provider.postal_code = provider.postal_code
        db_provider.address_confidence = provider.address_confidence
        db_provider.taxonomy = provider.taxonomy
        db_provider.credentials_json = provider.credentials.model_dump() if provider.credentials else None
        db_provider.licenses_json = [lic.model_dump() for lic in provider.licenses] if provider.licenses else []
        db_provider.network_affiliations = provider.network_affiliations
        db_provider.facility_affiliations = provider.facility_affiliations
        db_provider.services_offered = provider.services_offered
        db_provider.appointment_availability = provider.appointment_availability
        db_provider.website = provider.website
        db_provider.google_places_id = provider.google_places_id
        db_provider.validation_status = provider.validation_status.value
        db_provider.overall_confidence = provider.overall_confidence
        db_provider.data_element_confidences_json = [de.model_dump() for de in provider.data_element_confidences]
        db_provider.last_validated = datetime.utcnow()
        db_provider.validation_notes_json = provider.validation_notes
        db_provider.requires_manual_review = provider.requires_manual_review
        db_provider.review_priority = provider.review_priority
        db_provider.discrepancies_json = provider.discrepancies
        db_provider.updated_at = datetime.utcnow()
        
        await self.session.flush()
        return db_provider
    
    async def list_by_status(self, status: ValidationStatus, limit: int = 100) -> List[ProviderModel]:
        """List providers by validation status."""
        result = await self.session.execute(
            select(ProviderModel)
            .where(ProviderModel.validation_status == status.value)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_requiring_review(self, limit: int = 100) -> List[ProviderModel]:
        """List providers requiring manual review, ordered by priority."""
        result = await self.session.execute(
            select(ProviderModel)
            .where(ProviderModel.requires_manual_review == True)
            .order_by(ProviderModel.review_priority.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def create_validation_record(self, provider_id: str, validation_type: str, 
                                     status: str, confidence_score: float,
                                     data_before: dict, data_after: dict,
                                     discrepancies: List[str], validated_by: str,
                                     notes: Optional[str] = None):
        """Create a validation record."""
        from ..database.models import ValidationRecordModel
        record = ValidationRecordModel(
            provider_id=provider_id,
            validation_type=validation_type,
            status=status,
            confidence_score=confidence_score,
            data_before=data_before,
            data_after=data_after,
            discrepancies=discrepancies,
            validated_by=validated_by,
            notes=notes,
        )
        self.session.add(record)
        await self.session.flush()
        return record


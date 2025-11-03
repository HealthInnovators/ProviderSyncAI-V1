"""Workflow API routes."""
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from ...domain.enriched_entities import EnrichedProvider, ValidationBatch, ValidationReport
from ...application.use_cases.contact_validation_workflow import ContactValidationWorkflow
from ...application.use_cases.credential_verification_workflow import CredentialVerificationWorkflow
from ...application.use_cases.quality_assessment_workflow import QualityAssessmentWorkflow
from ...infrastructure.services.orchestrator import AgentOrchestrator
from ...infrastructure.models.grok_model import GrokModel
from ...infrastructure.services.pdf_extractor import PDFExtractorService
from ...infrastructure.database import get_db
from ...infrastructure.repositories.provider_repository import ProviderRepository
from ...infrastructure.logging import get_logger
from .schemas import ProviderSearchRequest
import json


router = APIRouter()
logger = get_logger(__name__)


def _get_orchestrator() -> AgentOrchestrator:
    """Get orchestrator instance."""
    from ...infrastructure.settings import settings
    if settings.grok_api_key:
        model = GrokModel(api_key=settings.grok_api_key)
        return AgentOrchestrator(model)
    raise HTTPException(status_code=500, detail="Grok API key not configured")


@router.post("/workflows/contact-validation/batch")
async def batch_contact_validation(providers: List[dict]) -> dict:
    """Batch contact validation workflow."""
    try:
        # Convert dicts to EnrichedProvider
        enriched_providers = [EnrichedProvider(**p) for p in providers]
        
        orchestrator = _get_orchestrator()
        workflow = ContactValidationWorkflow(orchestrator)
        batch = await workflow.execute_batch(enriched_providers)
        
        return {
            "batch_id": batch.batch_id,
            "status": batch.status,
            "total_providers": batch.total_providers,
            "processed_count": batch.processed_count,
            "validated_count": batch.validated_count,
            "discrepancy_count": batch.discrepancy_count,
            "requires_review_count": batch.requires_review_count,
        }
    except Exception as e:
        logger.error("batch_validation_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/credential-verification")
async def credential_verification(provider: dict) -> dict:
    """Credential verification workflow."""
    try:
        enriched_provider = EnrichedProvider(**provider)
        
        orchestrator = _get_orchestrator()
        workflow = CredentialVerificationWorkflow(orchestrator)
        verified = await workflow.verify_provider_credentials(enriched_provider)
        
        return {
            "npi": verified.npi,
            "validation_status": verified.validation_status.value,
            "overall_confidence": verified.overall_confidence,
            "requires_manual_review": verified.requires_manual_review,
        }
    except Exception as e:
        logger.error("credential_verification_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/quality-assessment")
async def quality_assessment(provider_npis: List[str]) -> dict:
    """Quality assessment workflow."""
    try:
        orchestrator = _get_orchestrator()
        workflow = QualityAssessmentWorkflow(orchestrator)
        report = await workflow.assess_directory_quality(provider_npis)
        
        return {
            "report_id": report.report_id,
            "generated_at": report.generated_at.isoformat(),
            "summary": report.summary,
            "providers_validated": report.providers_validated,
            "providers_with_discrepancies": report.providers_with_discrepancies,
            "providers_requiring_review": report.providers_requiring_review,
            "recommendations": report.recommendations,
        }
    except Exception as e:
        logger.error("quality_assessment_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)) -> dict:
    """Extract provider data from PDF."""
    try:
        from ...infrastructure.settings import settings
        
        # Save uploaded file temporarily
        import aiofiles
        import os
        temp_path = f"/tmp/{file.filename}"
        
        async with aiofiles.open(temp_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Extract using PDF service
        model = GrokModel(api_key=settings.grok_api_key) if settings.grok_api_key else None
        extractor = PDFExtractorService(model)
        data = await extractor.extract_provider_data(temp_path)
        
        # Cleanup
        os.remove(temp_path)
        
        return {"extracted_data": data}
    except Exception as e:
        logger.error("pdf_extraction_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflows/review-queue")
async def get_review_queue(limit: int = 50) -> dict:
    """Get providers requiring manual review."""
    try:
        db = get_db()
        async with db.get_session() as session:
            repo = ProviderRepository(session)
            providers = await repo.list_requiring_review(limit)
            
            return {
                "count": len(providers),
                "providers": [
                    {
                        "npi": p.npi,
                        "name": f"{p.first_name} {p.last_name}" if p.first_name else p.organization_name,
                        "priority": p.review_priority,
                        "discrepancies": p.discrepancies_json,
                        "validation_status": p.validation_status,
                    }
                    for p in providers
                ]
            }
    except Exception as e:
        logger.error("review_queue_failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


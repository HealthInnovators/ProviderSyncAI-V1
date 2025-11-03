"""Extended domain entities for provider data validation."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ValidationStatus(str, Enum):
    """Provider validation status."""
    PENDING = "pending"
    VALIDATED = "validated"
    DISCREPANCY = "discrepancy"
    REQUIRES_REVIEW = "requires_review"
    FLAGGED = "flagged"


class DataSource(str, Enum):
    """Data source types."""
    NPPES = "nppes"
    WEB_SCRAPING = "web_scraping"
    STATE_LICENSING = "state_licensing"
    GOOGLE_MAPS = "google_maps"
    PROVIDER_WEBSITE = "provider_website"
    PDF_EXTRACTION = "pdf_extraction"


class DataElementConfidence(BaseModel):
    """Confidence score for a data element."""
    element_name: str
    value: Optional[str] = None
    confidence_score: float = Field(ge=0.0, le=1.0)
    source: DataSource
    verified_at: Optional[datetime] = None
    cross_validated: bool = False
    discrepancy_found: bool = False


class ProviderLicense(BaseModel):
    """Provider license information."""
    license_number: str
    state: str
    license_type: str
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    status: str
    disciplinary_actions: List[Dict[str, Any]] = []


class ProviderCredential(BaseModel):
    """Provider credential information."""
    education: List[str] = []
    board_certifications: List[str] = []
    specialties: List[str] = []
    years_of_experience: Optional[int] = None


class EnrichedProvider(BaseModel):
    """Extended provider model with validation data."""
    npi: str
    enumeration_type: str
    
    # Basic demographics
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_name: Optional[str] = None
    
    # Contact information with confidence
    phone: Optional[str] = None
    phone_confidence: float = 0.0
    email: Optional[str] = None
    email_confidence: float = 0.0
    
    # Address information
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    address_confidence: float = 0.0
    
    # Professional details
    taxonomy: Optional[str] = None
    credentials: Optional[ProviderCredential] = None
    licenses: List[ProviderLicense] = []
    
    # Network and affiliations
    network_affiliations: List[str] = []
    facility_affiliations: List[str] = []
    
    # Services and availability
    services_offered: List[str] = []
    appointment_availability: Optional[bool] = None
    
    # Website and online presence
    website: Optional[str] = None
    google_places_id: Optional[str] = None
    
    # Validation metadata
    validation_status: ValidationStatus = ValidationStatus.PENDING
    overall_confidence: float = 0.0
    data_element_confidences: List[DataElementConfidence] = []
    last_validated: Optional[datetime] = None
    validation_notes: List[str] = []
    
    # Flags
    requires_manual_review: bool = False
    review_priority: int = 0  # Higher = more urgent
    discrepancies: List[str] = []


class ValidationBatch(BaseModel):
    """Batch validation job."""
    batch_id: str
    total_providers: int
    processed_count: int = 0
    validated_count: int = 0
    discrepancy_count: int = 0
    requires_review_count: int = 0
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str = "pending"
    providers: List[EnrichedProvider] = []


class QualityMetric(BaseModel):
    """Data quality metrics."""
    metric_name: str
    value: float
    threshold: Optional[float] = None
    trend: Optional[str] = None  # "improving", "declining", "stable"
    measured_at: datetime


class ValidationReport(BaseModel):
    """Validation report."""
    report_id: str
    batch_id: Optional[str] = None
    generated_at: datetime
    summary: Dict[str, Any]
    providers_validated: int
    providers_with_discrepancies: int
    providers_requiring_review: int
    quality_metrics: List[QualityMetric] = []
    prioritized_review_list: List[EnrichedProvider] = []
    recommendations: List[str] = []


class EmailTemplate(BaseModel):
    """Email template for provider communication."""
    template_id: str
    subject: str
    body: str
    provider_npi: str
    generated_at: datetime


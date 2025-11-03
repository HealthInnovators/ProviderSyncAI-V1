"""SQLAlchemy database models."""
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class ProviderModel(Base):
    """Provider database model."""
    __tablename__ = "providers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    npi = Column(String, unique=True, nullable=False, index=True)
    enumeration_type = Column(String)
    
    # Basic demographics
    first_name = Column(String)
    last_name = Column(String)
    organization_name = Column(String)
    
    # Contact information
    phone = Column(String)
    phone_confidence = Column(Float, default=0.0)
    email = Column(String)
    email_confidence = Column(Float, default=0.0)
    
    # Address
    address_line1 = Column(String)
    address_line2 = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    address_confidence = Column(Float, default=0.0)
    
    # Professional details
    taxonomy = Column(String)
    credentials_json = Column(JSON)
    licenses_json = Column(JSON)
    
    # Network and services
    network_affiliations = Column(JSON, default=list)
    facility_affiliations = Column(JSON, default=list)
    services_offered = Column(JSON, default=list)
    appointment_availability = Column(Boolean)
    
    # Online presence
    website = Column(String)
    google_places_id = Column(String)
    
    # Validation metadata
    validation_status = Column(String, default="pending")
    overall_confidence = Column(Float, default=0.0)
    data_element_confidences_json = Column(JSON, default=list)
    last_validated = Column(DateTime)
    validation_notes_json = Column(JSON, default=list)
    
    # Flags
    requires_manual_review = Column(Boolean, default=False)
    review_priority = Column(Integer, default=0)
    discrepancies_json = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    validations = relationship("ValidationRecordModel", back_populates="provider")


class ValidationRecordModel(Base):
    """Validation record tracking."""
    __tablename__ = "validation_records"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider_id = Column(String, ForeignKey("providers.id"), nullable=False)
    batch_id = Column(String, index=True)
    
    validation_type = Column(String)  # "contact", "credential", "quality_assessment"
    status = Column(String)
    confidence_score = Column(Float)
    
    data_before = Column(JSON)
    data_after = Column(JSON)
    discrepancies = Column(JSON, default=list)
    
    validated_by = Column(String)  # "agent_name" or "human"
    validated_at = Column(DateTime, default=datetime.utcnow)
    
    notes = Column(Text)
    
    # Relationships
    provider = relationship("ProviderModel", back_populates="validations")


class BatchJobModel(Base):
    """Batch processing job."""
    __tablename__ = "batch_jobs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    batch_id = Column(String, unique=True, nullable=False, index=True)
    
    job_type = Column(String)  # "contact_validation", "credential_verification", "quality_assessment"
    total_providers = Column(Integer)
    processed_count = Column(Integer, default=0)
    validated_count = Column(Integer, default=0)
    discrepancy_count = Column(Integer, default=0)
    requires_review_count = Column(Integer, default=0)
    
    status = Column(String, default="pending")  # "pending", "processing", "completed", "failed"
    
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    error_message = Column(Text)
    metadata_json = Column(JSON)


class QualityMetricModel(Base):
    """Quality metrics tracking."""
    __tablename__ = "quality_metrics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    metric_name = Column(String, nullable=False, index=True)
    value = Column(Float, nullable=False)
    threshold = Column(Float)
    trend = Column(String)
    measured_at = Column(DateTime, default=datetime.utcnow, index=True)
    metadata_json = Column(JSON)


class ReviewQueueModel(Base):
    """Priority queue for manual review."""
    __tablename__ = "review_queue"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider_id = Column(String, ForeignKey("providers.id"), nullable=False)
    priority = Column(Integer, default=0, index=True)
    reason = Column(String)
    assigned_to = Column(String)
    status = Column(String, default="pending")  # "pending", "in_progress", "resolved"
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)


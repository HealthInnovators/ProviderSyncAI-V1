"""Email generation service."""
from typing import Dict, Any
from jinja2 import Template
from ...domain.enriched_entities import EnrichedProvider, EmailTemplate
from datetime import datetime
import uuid


class EmailService:
    """Service for generating provider communication emails."""
    
    # Email templates
    VALIDATION_REQUEST_TEMPLATE = """
Subject: Provider Directory Update Request - {{ provider_name }}

Dear {{ provider_name }},

We are reaching out to verify and update your information in our provider directory.

Current Information:
- Name: {{ provider.first_name }} {{ provider.last_name }}
- NPI: {{ provider.npi }}
- Address: {{ provider.address_line1 }}, {{ provider.city }}, {{ provider.state }}
- Phone: {{ provider.phone or 'Not on file' }}
- Email: {{ provider.email or 'Not on file' }}

Please review and confirm this information is accurate, or provide any necessary updates.

Thank you for helping us maintain accurate provider information.

Best regards,
Provider Directory Management Team
"""
    
    DISCREPANCY_NOTIFICATION_TEMPLATE = """
Subject: Provider Directory Discrepancy - Action Required

Dear {{ provider_name }},

We have detected discrepancies in your provider directory information:

{{ discrepancies }}

Please review and update your information as soon as possible.

Thank you,
Provider Directory Management Team
"""
    
    def generate_validation_email(self, provider: EnrichedProvider) -> EmailTemplate:
        """Generate validation request email."""
        template = Template(self.VALIDATION_REQUEST_TEMPLATE)
        
        provider_name = f"{provider.first_name} {provider.last_name}" if provider.first_name else provider.organization_name or "Provider"
        
        body = template.render(
            provider_name=provider_name,
            provider=provider,
        )
        
        subject = f"Provider Directory Update Request - {provider_name}"
        
        return EmailTemplate(
            template_id=str(uuid.uuid4()),
            subject=subject,
            body=body,
            provider_npi=provider.npi,
            generated_at=datetime.utcnow(),
        )
    
    def generate_discrepancy_email(self, provider: EnrichedProvider) -> EmailTemplate:
        """Generate discrepancy notification email."""
        template = Template(self.DISCREPANCY_NOTIFICATION_TEMPLATE)
        
        provider_name = f"{provider.first_name} {provider.last_name}" if provider.first_name else provider.organization_name or "Provider"
        
        discrepancies_text = "\n".join(f"- {d}" for d in provider.discrepancies)
        
        body = template.render(
            provider_name=provider_name,
            discrepancies=discrepancies_text,
        )
        
        subject = f"Provider Directory Discrepancy - Action Required - {provider_name}"
        
        return EmailTemplate(
            template_id=str(uuid.uuid4()),
            subject=subject,
            body=body,
            provider_npi=provider.npi,
            generated_at=datetime.utcnow(),
        )


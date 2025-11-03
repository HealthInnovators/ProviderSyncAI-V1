"""Confidence scoring service for data validation."""
from typing import List, Dict, Any, Optional
from ...domain.enriched_entities import DataElementConfidence, DataSource
from datetime import datetime


class ConfidenceScoringService:
    """Service for calculating confidence scores."""
    
    # Source reliability weights (higher = more reliable)
    SOURCE_WEIGHTS = {
        DataSource.NPPES: 0.9,
        DataSource.STATE_LICENSING: 0.85,
        DataSource.WEB_SCRAPING: 0.7,
        DataSource.PROVIDER_WEBSITE: 0.75,
        DataSource.GOOGLE_MAPS: 0.65,
        DataSource.PDF_EXTRACTION: 0.6,
    }
    
    @staticmethod
    def calculate_element_confidence(
        value: Optional[str],
        source: DataSource,
        cross_validated: bool = False,
        discrepancy_found: bool = False,
    ) -> float:
        """Calculate confidence score for a data element."""
        if not value:
            return 0.0
        
        if discrepancy_found:
            return 0.3  # Low confidence if discrepancy found
        
        base_confidence = ConfidenceScoringService.SOURCE_WEIGHTS.get(source, 0.5)
        
        # Boost if cross-validated
        if cross_validated:
            base_confidence = min(1.0, base_confidence * 1.15)
        
        # Normalize value quality (non-empty, reasonable length)
        if len(value.strip()) < 3:
            base_confidence *= 0.7
        
        return round(base_confidence, 2)
    
    @staticmethod
    def calculate_overall_confidence(element_confidences: List[DataElementConfidence]) -> float:
        """Calculate overall confidence score for provider."""
        if not element_confidences:
            return 0.0
        
        # Weighted average based on element importance
        weights = {
            "phone": 0.2,
            "email": 0.15,
            "address": 0.25,
            "license": 0.2,
            "taxonomy": 0.15,
            "website": 0.05,
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for conf in element_confidences:
            weight = weights.get(conf.element_name.lower(), 0.1)
            total_score += conf.confidence_score * weight
            total_weight += weight
        
        return round(total_score / total_weight if total_weight > 0 else 0.0, 2)
    
    @staticmethod
    def cross_validate_elements(
        elements: List[DataElementConfidence]
    ) -> List[DataElementConfidence]:
        """Cross-validate elements and update confidence scores."""
        # Group by element name
        element_groups: Dict[str, List[DataElementConfidence]] = {}
        for element in elements:
            name = element.element_name
            if name not in element_groups:
                element_groups[name] = []
            element_groups[name].append(element)
        
        validated_elements = []
        for name, group in element_groups.items():
            if len(group) == 1:
                # Single source, no cross-validation
                validated_elements.append(group[0])
            else:
                # Multiple sources - check for agreement
                values = [e.value for e in group if e.value]
                unique_values = set(values)
                
                if len(unique_values) == 1:
                    # All sources agree - high confidence
                    for e in group:
                        e.cross_validated = True
                        e.confidence_score = min(1.0, e.confidence_score * 1.2)
                        validated_elements.append(e)
                elif len(unique_values) == 2:
                    # Some disagreement - moderate confidence
                    for e in group:
                        e.discrepancy_found = True
                        e.confidence_score = max(0.4, e.confidence_score * 0.7)
                        validated_elements.append(e)
                else:
                    # High disagreement - low confidence, flag for review
                    for e in group:
                        e.discrepancy_found = True
                        e.confidence_score = 0.3
                        validated_elements.append(e)
        
        return validated_elements


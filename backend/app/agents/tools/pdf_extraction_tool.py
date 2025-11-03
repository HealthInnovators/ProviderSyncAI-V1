"""PDF extraction tool for agents."""
from smolagents import Tool
from ...infrastructure.services.pdf_extractor import PDFExtractorService
from ...infrastructure.logging import get_logger


logger = get_logger(__name__)


class PDFExtractionTool(Tool):
    """Extract provider data from PDF documents."""
    
    name = "extract_from_pdf"
    description = "Extract provider information from PDF documents using text extraction and VLM"
    inputs = {"pdf_path": str}
    output_type = "json"
    
    def __init__(self, pdf_extractor: PDFExtractorService):
        super().__init__()
        self.pdf_extractor = pdf_extractor
    
    async def __call__(self, pdf_path: str):
        """Extract data from PDF."""
        try:
            data = await self.pdf_extractor.extract_provider_data(pdf_path)
            return data
        except Exception as e:
            logger.error("pdf_extraction_failed", path=pdf_path, error=str(e))
            return {"error": str(e)}


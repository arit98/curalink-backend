from pydantic import BaseModel
from typing import Optional, Dict, Any

class PDFExtractRequest(BaseModel):
    model: str
    prompt: str
    text: str

class PDFExtractResponse(BaseModel):
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    estimated_time: Optional[float] = None


from fastapi import APIRouter, HTTPException
import httpx
import json
import re
from app.schemas.pdf_schema import PDFExtractRequest, PDFExtractResponse
from app.core.config import settings

router = APIRouter()

@router.post("/extract-metadata", response_model=PDFExtractResponse)
async def extract_pdf_metadata(request: PDFExtractRequest):
    """
    Extract metadata using HuggingFace Router API (hf-inference).
    """

    api_key = settings.HUGGINGFACE_API_KEY
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Hugging Face API key not configured."
        )

    url = f"https://router.huggingface.co/hf-inference/models/{request.model}"

    payload = {
        "inputs": request.prompt + "\n\nPDF TEXT:\n" + request.text,
        "parameters": {
            "max_new_tokens": 1500,
            "temperature": 0.1,
            "return_full_text": False,
            "top_p": 0.95,
        }
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=80.0) as client:
            response = await client.post(url, headers=headers, json=payload)

        # ✔ HF router returns 503 when model is loading
        if response.status_code == 503:
            err = response.json()
            return PDFExtractResponse(
                error=err.get("error", "Model is loading"),
                estimated_time=err.get("estimated_time")
            )

        if not response.is_success:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Hugging Face API error: {response.text}"
            )

        data = response.json()

        # --- Parse output ---
        generated = ""
        if isinstance(data, list) and len(data) > 0:
            generated = data[0].get("generated_text", "") or data[0].get("text", "")
        elif isinstance(data, dict):
            generated = data.get("generated_text", "") or data.get("text", "")

        if not generated:
            raise HTTPException(
                status_code=500,
                detail=f"No generated_text in HF response: {data}"
            )

        # --- Clean markdown & extract JSON ---
        cleaned = (
            generated.replace("```json", "")
                     .replace("```", "")
                     .strip()
        )

        match = re.search(r"\{[\s\S]*\}", cleaned)

        if not match:
            raise HTTPException(
                status_code=500,
                detail=f"No JSON found in model output. Raw: {cleaned[:400]}"
            )

        metadata = json.loads(match.group(0))
        return PDFExtractResponse(metadata=metadata)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
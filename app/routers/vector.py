from fastapi import APIRouter, Depends, HTTPException
from transformers import AutoTokenizer, AutoModel

import torch

from app.dependencies import getApplicationToken
from app.models import TextToVectorRequest

router = APIRouter()

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

router = APIRouter(
    prefix="/vector",
    tags=["vector"],
    dependencies=[Depends(getApplicationToken)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}
@router.get("/")
async def read_items():
    return fake_items_db


@router.post("/generate", tags=["vector"])
def generate(request: TextToVectorRequest):
    try:
        inputs = tokenizer(request.text, return_tensors="pt", truncation=True, padding=True)
        
        with torch.no_grad():
            outputs = model(**inputs)
            embedding = torch.mean(outputs.last_hidden_state, dim=1).squeeze().tolist()
        
        return {"embedding": embedding}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

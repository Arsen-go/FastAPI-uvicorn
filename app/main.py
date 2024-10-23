from fastapi import FastAPI, HTTPException, Depends
from transformers import AutoTokenizer, AutoModel
import torch

from app.models import TextToVectorRequest

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

app = FastAPI()

@app.get("/")
def testApp():
    return {"message": "App is running"}

@app.post("/createVector/")
def createVector(request: TextToVectorRequest):
    try:
        inputs = tokenizer(request.text, return_tensors="pt", truncation=True, padding=True)
        
        with torch.no_grad():
            outputs = model(**inputs)
            embedding = torch.mean(outputs.last_hidden_state, dim=1).squeeze().tolist()
        
        return {"embedding": embedding}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



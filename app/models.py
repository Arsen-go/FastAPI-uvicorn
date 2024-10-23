from pydantic import BaseModel

class TextToVectorRequest(BaseModel):
    text: str
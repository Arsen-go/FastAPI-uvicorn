from fastapi import Depends, FastAPI

from app.dependencies import getApplicationToken
from .routers import vector


app = FastAPI()

app = FastAPI(dependencies=[Depends(getApplicationToken)])

app.include_router(vector.router)


@app.get("/")
def testApp():
    return {"message": "App is running"}



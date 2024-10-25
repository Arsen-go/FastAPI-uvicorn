from typing import Annotated

from fastapi import Header, HTTPException

async def getApplicationToken(x_token: Annotated[str, Header(alias="x-token")]):
    print(x_token)
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


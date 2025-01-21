from fastapi import HTTPException, Header, status
from app.core.config import settings

def identify_third_party_request(
    authentication_token: str | None = Header(None, alias="X-Auth"),
):
    """Identifies if the request is coming from a third party."""
    if authentication_token and authentication_token==settings.AUTH_TOKEN:
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token."
        )

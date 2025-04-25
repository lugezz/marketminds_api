from fastapi import APIRouter
# from fastapi import APIRouter, Depends, HTTPException
# from sqlmodel import select, Session

# from api.db.session import get_session
# from api.marketminds.models import (
#     ProvinciaModel,
# )


router = APIRouter()


@router.get("/healtz/")
def health_check():
    """ Health check endpoint.
    """
    return {"status": "ok"}

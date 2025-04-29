from fastapi import APIRouter
# from fastapi import APIRouter, Depends, HTTPException
# from sqlmodel import select, Session

# from api.db.session import get_session
# from api.marketminds.models import (
#     ProvinciaModel,
# )
from api.import_dataset.tools import import_dataset


router = APIRouter()


@router.get("/healtz/")
def health_check():
    """ Health check endpoint.
    """
    return {"status": "ok"}


@router.get("/import-dataset/")
def import_data():
    """ Import data from CSV file.
    """
    import_result = import_dataset()
    if import_result["status"] != 200:
        return {
            "status": import_result["status"],
            "message": import_result["message"]
        }

    return import_result

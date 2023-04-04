from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/path",
    summary="Description endpoint.",
    description="Description request endpoint.",
    response_description="Description response endpoint.",
)
async def path() -> bool:
    return True
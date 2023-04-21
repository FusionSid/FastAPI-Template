from fastapi import APIRouter
from fastapi.responses import RedirectResponse

example_router = APIRouter(
    tags=[
        "Example",
    ],
)


@example_router.get("/")
async def redirect_to_docs():
    return RedirectResponse("/docs")

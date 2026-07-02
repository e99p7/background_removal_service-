from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.inference import remove_background
from app.utils import read_and_validate_upload

app = FastAPI(
    title="Background Removal Service",
    description="Remove image backgrounds and return transparent PNG files.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post(
    "/remove-background",
    responses={
        200: {"content": {"image/png": {}}},
        400: {"description": "Invalid image"},
        413: {"description": "Image too large"},
        415: {"description": "Unsupported media type"},
    },
)
async def remove_background_endpoint(file: UploadFile = File(...)) -> Response:
    image_bytes = await read_and_validate_upload(file)
    png_bytes = remove_background(image_bytes)
    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=background_removed.png"},
    )

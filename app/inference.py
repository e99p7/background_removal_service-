from functools import lru_cache
from io import BytesIO

from PIL import Image
from rembg import new_session, remove

from app.schemas import settings


@lru_cache(maxsize=1)
def get_session():
    """Create and cache the rembg model session.

    The first call may download model weights into the local cache.
    """

    return new_session(settings.rembg_model)


def remove_background(image_bytes: bytes) -> bytes:
    """Remove background and return PNG bytes with alpha channel."""

    with Image.open(BytesIO(image_bytes)) as img:
        rgb_image = img.convert("RGB")

    result = remove(rgb_image, session=get_session())

    if isinstance(result, bytes):
        return result

    buffer = BytesIO()
    result.save(buffer, format="PNG")
    return buffer.getvalue()

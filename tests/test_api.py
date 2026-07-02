from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def make_test_image() -> bytes:
    image = Image.new("RGB", (64, 64), "white")
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Background Removal Service" in response.text


def test_remove_background_endpoint(monkeypatch):
    def fake_remove_background(_: bytes) -> bytes:
        image = Image.new("RGBA", (32, 32), (255, 0, 0, 128))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()

    monkeypatch.setattr("app.main.remove_background", fake_remove_background)

    response = client.post(
        "/remove-background",
        files={"file": ("test.jpg", make_test_image(), "image/jpeg")},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.content.startswith(b"\x89PNG")


def test_unsupported_file_type():
    response = client.post(
        "/remove-background",
        files={"file": ("test.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415

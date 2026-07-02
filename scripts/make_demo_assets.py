"""Generate lightweight demo images for README without external assets."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
DOCS = ROOT / "docs"
EXAMPLES.mkdir(exist_ok=True)
DOCS.mkdir(exist_ok=True)


def font(size: int):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def make_input():
    img = Image.new("RGB", (900, 600), (225, 232, 242))
    d = ImageDraw.Draw(img)
    for x in range(0, 900, 60):
        d.line((x, 0, x - 300, 600), fill=(205, 214, 228), width=3)
    d.rounded_rectangle((340, 130, 560, 500), radius=95, fill=(34, 79, 170))
    d.ellipse((370, 70, 530, 230), fill=(245, 188, 126))
    d.rectangle((415, 230, 485, 300), fill=(245, 188, 126))
    d.text((28, 28), "example/input.jpg", fill=(23, 32, 51), font=font(30))
    img.save(EXAMPLES / "input.jpg", quality=92)
    return img


def checkerboard(size):
    img = Image.new("RGBA", size, (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    tile = 32
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if (x // tile + y // tile) % 2 == 0:
                d.rectangle((x, y, x + tile, y + tile), fill=(226, 226, 226, 255))
    return img


def make_output():
    img = Image.new("RGBA", (900, 600), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((340, 130, 560, 500), radius=95, fill=(34, 79, 170, 255))
    d.ellipse((370, 70, 530, 230), fill=(245, 188, 126, 255))
    d.rectangle((415, 230, 485, 300), fill=(245, 188, 126, 255))
    img.save(EXAMPLES / "output.png")
    return img


def make_demo(input_img, output_img):
    canvas = Image.new("RGB", (1400, 720), (248, 250, 253))
    d = ImageDraw.Draw(canvas)
    d.text((70, 50), "Background Removal Service", fill=(23, 32, 51), font=font(48))
    d.text((70, 112), "FastAPI + rembg baseline", fill=(82, 99, 122), font=font(28))

    left = input_img.resize((520, 347))
    right_bg = checkerboard((520, 347)).convert("RGBA")
    person = output_img.resize((520, 347))
    right_bg.alpha_composite(person)
    right = right_bg.convert("RGB")

    d.rounded_rectangle((70, 190, 630, 590), radius=28, fill=(255, 255, 255), outline=(220, 226, 236), width=2)
    d.rounded_rectangle((770, 190, 1330, 590), radius=28, fill=(255, 255, 255), outline=(220, 226, 236), width=2)
    canvas.paste(left, (90, 230))
    canvas.paste(right, (790, 230))
    d.text((90, 200), "Original", fill=(23, 32, 51), font=font(26))
    d.text((790, 200), "Transparent PNG", fill=(23, 32, 51), font=font(26))
    d.text((667, 360), "→", fill=(23, 32, 51), font=font(64))
    canvas.save(DOCS / "demo.png")


def make_architecture():
    canvas = Image.new("RGB", (1200, 520), (248, 250, 253))
    d = ImageDraw.Draw(canvas)
    d.text((60, 50), "Architecture", fill=(23, 32, 51), font=font(46))
    boxes = [
        ("Client", 70),
        ("FastAPI", 320),
        ("Validation", 570),
        ("rembg / U²-Net", 820),
    ]
    for label, x in boxes:
        d.rounded_rectangle((x, 200, x + 220, 320), radius=22, fill=(255, 255, 255), outline=(220, 226, 236), width=2)
        d.text((x + 35, 242), label, fill=(23, 32, 51), font=font(24))
    for x in [290, 540, 790]:
        d.text((x, 238), "→", fill=(23, 32, 51), font=font(42))
    d.text((840, 360), "PNG with alpha", fill=(82, 99, 122), font=font(26))
    canvas.save(DOCS / "architecture.png")


if __name__ == "__main__":
    inp = make_input()
    out = make_output()
    make_demo(inp, out)
    make_architecture()

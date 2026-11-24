# -*- coding: utf-8 -*-
"""โหลดรูปความทรงจำ + ใบหน้า → ย่อ/ครอป → data URI (ไม่ต้องใช้ Streamlit ในไฟล์นี้)"""
from __future__ import annotations

import base64
import io
import json
import re
from pathlib import Path

from PIL import Image, ImageOps

import config as C

try:  # รองรับรูป HEIC จาก iPhone ถ้าติดตั้ง pillow-heif ไว้
    import pillow_heif  # type: ignore

    pillow_heif.register_heif_opener()
except Exception:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parent
PHOTO_DIR = ROOT / "assets" / "photos"
FACE_DIR = ROOT / "assets" / "faces"
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}


def _natural_key(p: Path):
    return [int(s) if s.isdigit() else s.lower() for s in re.split(r"(\d+)", p.name)]


def _data_uri(img: Image.Image, quality: int) -> str:
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def list_photo_files() -> list[Path]:
    if not PHOTO_DIR.exists():
        return []
    files = [p for p in PHOTO_DIR.iterdir() if p.suffix.lower() in IMG_EXT and not p.name.startswith(".")]
    return sorted(files, key=_natural_key)


def photos_signature() -> tuple:
    """ใช้เป็น key ของ cache: เปลี่ยนเมื่อมีการเพิ่ม/ลบ/แก้ไฟล์รูป"""
    sig = [(p.name, p.stat().st_mtime_ns) for p in list_photo_files()]
    cap = PHOTO_DIR / "captions.json"
    if cap.exists():
        sig.append(("captions.json", cap.stat().st_mtime_ns))
    return tuple(sig)


def _load_captions() -> dict:
    cap = PHOTO_DIR / "captions.json"
    if cap.exists():
        try:
            return json.loads(cap.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _placeholder(i: int) -> str:
    palettes = [("#ffd6e7", "#c9b6ff"), ("#ffe9b8", "#ffb3cf"), ("#c9e7ff", "#d3c3ff"), ("#d4f5dc", "#ffe9b8")]
    a, b = palettes[i % len(palettes)]
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='400' height='500' viewBox='0 0 400 500'>"
        f"<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{a}'/>"
        f"<stop offset='1' stop-color='{b}'/></linearGradient></defs>"
        "<rect width='400' height='500' fill='url(#g)'/>"
        "<path d='M200 330 C110 262 120 190 165 190 C186 190 198 204 200 214 C202 204 214 190 235 190 "
        "C280 190 290 262 200 330Z' fill='#ff7aa8' fill-opacity='.85'/>"
        f"<text x='200' y='410' font-size='30' text-anchor='middle' fill='#6b4a8a' font-family='sans-serif'>photo {i + 1}</text>"
        "</svg>"
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def load_photos() -> tuple[list[dict], bool]:
    """คืน ([{src, cap}, ...], is_placeholder)"""
    files = list_photo_files()
    if not files:
        return [{"src": _placeholder(i), "cap": "", "ar": 0.8} for i in range(C.PLACEHOLDER_COUNT)], True
    caps = _load_captions()
    out = []
    for p in files:
        try:
            img = Image.open(p)
            img = ImageOps.exif_transpose(img)
            img.thumbnail((C.PHOTO_MAX_SIDE, C.PHOTO_MAX_SIDE))
            out.append({
                "src": _data_uri(img, C.PHOTO_QUALITY),
                "cap": str(caps.get(p.name, "")),
                "ar": round(img.width / img.height, 3),  # สัดส่วน กว้าง/สูง ให้ฉากทำกรอบโพลารอยด์ตามรูป
            })
        except Exception as e:  # ข้ามไฟล์ที่เปิดไม่ได้ (เช่น HEIC โดยไม่มี pillow-heif)
            print(f"[assets] ข้ามไฟล์ {p.name}: {e}")
    if not out:
        return [{"src": _placeholder(i), "cap": "", "ar": 0.8} for i in range(C.PLACEHOLDER_COUNT)], True
    return out, False


def face_signature() -> tuple:
    return tuple(
        (p.name, p.stat().st_mtime_ns) for p in sorted(FACE_DIR.glob("*")) if p.suffix.lower() in IMG_EXT
    ) if FACE_DIR.exists() else ()


def _find_face(key: str) -> Path | None:
    if not FACE_DIR.exists():
        return None
    for p in sorted(FACE_DIR.iterdir()):
        if p.stem.lower() == key and p.suffix.lower() in IMG_EXT:
            return p
    return None


def load_face(key: str) -> str | None:
    """key = 'me' | 'partner' → data URI สี่เหลี่ยมจัตุรัส (ให้ SVG ตัดเป็นวงกลมเอง) หรือ None ถ้ายังไม่มีไฟล์"""
    p = _find_face(key)
    if not p:
        return None
    try:
        img = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    except Exception as e:
        print(f"[assets] เปิดรูปหน้า {p.name} ไม่ได้: {e}")
        return None
    fx, fy, zoom = C.FACE_FOCUS.get(key, (0.5, 0.42, 1.0))
    w, h = img.size
    side = min(w, h) / max(1.0, zoom)
    cx = min(max(fx * w, side / 2), w - side / 2)
    cy = min(max(fy * h, side / 2), h - side / 2)
    box = (int(cx - side / 2), int(cy - side / 2), int(cx + side / 2), int(cy + side / 2))
    img = img.crop(box).resize((260, 260), Image.LANCZOS)
    return _data_uri(img, 86)


def load_faces() -> dict:
    return {"me": load_face("me"), "partner": load_face("partner")}

"""Optimasi gambar: (1) kecilkan/kompres foto saat diunggah; (2) thumbnail WebP on-demand ba kartu/lista.

- optimize_upload(): foto kamera HP (3-6 MB) -> maks 1600px, kualitas 82, biasanya < 400 KB.
- thumb_url(): buat salinan kecil sekali, simpan di MEDIA_ROOT/thumbs/, lalu pakai ulang.
Semua fungsi aman: jika gagal / format khusus (SVG, GIF animasi), kembali ke file asli."""
import hashlib
import io
import os

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageOps

MAX_UPLOAD_PX = 1600
SKIP_EXT = (".svg", ".gif")


def _ext(name):
    return os.path.splitext(name or "")[1].lower()


def optimize_upload(field_file, max_px=MAX_UPLOAD_PX, quality=82):
    """Panggil ba file baru (belum disimpan). Return True se file diganti."""
    if not field_file or getattr(field_file, "_committed", True):
        return False
    name = field_file.name or ""
    if _ext(name) in SKIP_EXT:
        return False
    try:
        field_file.file.seek(0)
        img = Image.open(field_file.file)
        img.load()
    except Exception:
        return False
    if getattr(img, "is_animated", False):
        return False
    img = ImageOps.exif_transpose(img)
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    resized = max(img.size) > max_px
    if resized:
        img.thumbnail((max_px, max_px), Image.LANCZOS)
    size_before = getattr(field_file.file, "size", None) or 0
    if not resized and size_before and size_before < 300 * 1024:
        return False  # sudah kecil, jangan diutak-atik
    buf = io.BytesIO()
    base = os.path.splitext(os.path.basename(name))[0]
    if has_alpha:
        img.save(buf, "PNG", optimize=True)
        new_name = base + ".png"
    else:
        img.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
        new_name = base + ".jpg"
    if size_before and buf.tell() >= size_before and not resized:
        return False  # hasil tidak lebih kecil
    field_file.save(new_name, ContentFile(buf.getvalue()), save=False)
    return True


def thumb_url(field_file, width=600):
    """URL thumbnail WebP lebar `width` (rasio asli). Fallback ke URL asli."""
    if not field_file:
        return ""
    try:
        original_url = field_file.url
        name = field_file.name
        if _ext(name) in SKIP_EXT:
            return original_url
        src_path = field_file.path
        mtime = int(os.path.getmtime(src_path))
        key = hashlib.md5(f"{name}:{mtime}:{width}".encode()).hexdigest()[:12]
        rel = f"thumbs/{os.path.splitext(os.path.basename(name))[0]}_{width}_{key}.webp"
        dest = os.path.join(settings.MEDIA_ROOT, rel)
        if not os.path.exists(dest):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with Image.open(src_path) as img:
                img = ImageOps.exif_transpose(img)
                if img.width <= width:
                    return original_url
                img.thumbnail((width, width * 3), Image.LANCZOS)
                img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB").save(dest, "WEBP", quality=80, method=4)
        return settings.MEDIA_URL + rel
    except Exception:
        try:
            return field_file.url
        except Exception:
            return ""

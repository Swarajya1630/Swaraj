"""
Rajmudra Asset Optimizer
=======================
Creates optimized Rajmudra assets for different UI elements.
Preserves original artwork while creating appropriate sizes.
"""

import os
from PIL import Image, ImageEnhance, ImageFilter


ASSETS_DIR = os.path.join(os.path.dirname(__file__), "branding")
SOURCE = os.path.join(ASSETS_DIR, "rajmudra_source.jpg")


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def optimize_for_widget(size=(120, 120)):
    """Optimize Rajmudra for compact floating widget."""
    img = Image.open(SOURCE)
    img = img.convert("RGBA")

    bg = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
    img = bg

    img = img.resize(size, Image.Resampling.LANCZOS)

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.1)

    output = os.path.join(ASSETS_DIR, "rajmudra_widget.png")
    img.save(output, "PNG", optimize=True)
    print(f"Created: {output} ({size[0]}x{size[1]})")
    return output


def optimize_for_expanded(size=(200, 200)):
    """Optimize Rajmudra for expanded window."""
    img = Image.open(SOURCE)
    img = img.convert("RGBA")

    bg = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
    img = bg

    img = img.resize(size, Image.Resampling.LANCZOS)

    output = os.path.join(ASSETS_DIR, "rajmudra_expanded.png")
    img.save(output, "PNG", optimize=True)
    print(f"Created: {output} ({size[0]}x{size[1]})")
    return output


def optimize_for_tray(size=(32, 32)):
    """Optimize Rajmudra for system tray icon."""
    img = Image.open(SOURCE)
    img = img.convert("RGBA")

    bg = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
    img = bg

    img = img.resize(size, Image.Resampling.LANCZOS)

    output = os.path.join(ASSETS_DIR, "rajmudra_tray.png")
    img.save(output, "PNG", optimize=True)
    print(f"Created: {output} ({size[0]}x{size[1]})")
    return output


def optimize_for_splash(size=(400, 400)):
    """Optimize Rajmudra for startup splash."""
    img = Image.open(SOURCE)
    img = img.convert("RGBA")

    bg = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
    img = bg

    img = img.resize(size, Image.Resampling.LANCZOS)

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)

    output = os.path.join(ASSETS_DIR, "rajmudra_splash.png")
    img.save(output, "PNG", optimize=True)
    print(f"Created: {output} ({size[0]}x{size[1]})")
    return output


def create_all():
    """Create all optimized assets."""
    ensure_dir(ASSETS_DIR)

    if not os.path.exists(SOURCE):
        print(f"Source not found: {SOURCE}")
        print("Please place the Rajmudra image in assets/branding/")
        return False

    print("Optimizing Rajmudra assets...")
    optimize_for_widget()
    optimize_for_expanded()
    optimize_for_tray()
    optimize_for_splash()

    # Copy source as the main rajmudra.png for backward compatibility
    main_output = os.path.join(os.path.dirname(ASSETS_DIR), "rajmudra.png")
    img = Image.open(SOURCE)
    img = img.convert("RGBA")
    img = img.resize((280, 280), Image.Resampling.LANCZOS)
    img.save(main_output, "PNG", optimize=True)
    print(f"Created: {main_output} (280x280)")

    print("All assets created!")
    return True


if __name__ == "__main__":
    create_all()

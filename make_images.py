"""Генерация иллюстраций для каталога.

Каждая функция рисует отдельный продукт с помощью PIL (ImageDraw).
Координаты указаны в пикселях на холсте 1000×1000.
Далее scene() комбинирует рисунки на фоне, применяет масштабирование и сохраняет.
"""

import os
import random
from functools import partial

from PIL import Image, ImageDraw

MEDIA = "media"


# ---------- Рисунки (координаты 0..1000) ----------


def cheese(d, front="#f4c542", top="#f9dd7a", side="#d9a520"):
    """Рисует треугольный кусок сыра с отверстиями."""
    d.polygon([(150, 520), (750, 520), (870, 420), (270, 420)], fill=top)
    d.rectangle((150, 520, 750, 760), fill=front)
    d.polygon([(750, 520), (870, 420), (870, 660), (750, 760)], fill=side)
    for box in [(230, 590, 310, 670), (450, 640, 540, 720), (600, 560, 670, 620)]:
        d.ellipse(box, fill=side)


def milk(d):
    """Рисует пакет молока."""
    d.rectangle((330, 380, 670, 820), fill="#ffffff", outline="#c9d3df", width=6)
    d.polygon([(330, 380), (670, 380), (600, 280), (400, 280)], fill="#e0e6ee")
    d.rectangle((330, 520, 670, 680), fill="#4a90d9")
    d.ellipse((460, 550, 540, 650), fill="#ffffff")


def kefir(d):
    """Рисует бутылку кефира."""
    d.rectangle((440, 220, 560, 370), fill="#f5f5f5", outline="#c9d3df", width=6)
    d.rounded_rectangle(
        (360, 340, 640, 840), radius=60, fill="#ffffff", outline="#c9d3df", width=6
    )
    d.rectangle((430, 180, 570, 230), fill="#2a9d8f")
    d.rectangle((360, 520, 640, 700), fill="#6bbf59")


def tomato(d):
    """Рисует помидор."""
    d.ellipse((200, 260, 800, 860), fill="#e63946")
    d.ellipse((300, 360, 380, 460), fill="#f28b93")
    d.polygon(
        [(500, 320), (400, 240), (470, 270), (500, 180), (530, 270), (600, 240)],
        fill="#2d9a4b",
    )


def cucumber(d):
    """Рисует огурец."""
    d.rounded_rectangle((150, 400, 850, 600), radius=100, fill="#3d9a4b")
    d.rounded_rectangle((200, 460, 800, 490), radius=15, fill="#7bcf86")
    for x, y in [(260, 540), (400, 430), (520, 545), (650, 435), (740, 530)]:
        d.ellipse((x, y, x + 24, y + 24), fill="#7bcf86")


def apple(d):
    """Рисует красное яблоко."""
    d.ellipse((220, 300, 520, 800), fill="#d62828")
    d.ellipse((480, 300, 780, 800), fill="#d62828")
    d.ellipse((290, 380, 350, 470), fill="#ee6a6a")
    d.rectangle((485, 190, 515, 340), fill="#6b4423")
    d.ellipse((520, 200, 660, 270), fill="#2d9a4b")


def banana(d):
    """Рисует банан."""
    d.arc((150, 50, 850, 750), start=20, end=160, fill="#f6d743", width=130)
    for x in (228, 772):
        d.ellipse((x - 28, 470, x + 28, 530), fill="#6b4423")


def loaf(d, body="#d9923b", slash="#f0c27a"):
    """Рисует буханку хлеба.

    Параметры body и slash позволяют менять цвет теста и надрезов.
    """
    d.rounded_rectangle((170, 450, 830, 780), radius=150, fill=body)
    d.ellipse((200, 330, 800, 620), fill=body)
    for x in (360, 480, 600):
        d.line([(x, 440), (x + 60, 540)], fill=slash, width=34)


def croissant(d):
    """Рисует круассан."""
    fill, edge = "#e0a040", "#b9772a"
    for box in [
        (130, 520, 330, 720),
        (680, 520, 880, 720),
        (260, 430, 500, 690),
        (500, 430, 740, 690),
        (390, 370, 610, 700),
    ]:
        d.ellipse(box, fill=fill, outline=edge, width=8)
    for x in (450, 500, 550):
        d.line([(x, 410), (x, 650)], fill=edge, width=6)


def bun(d):
    """Рисует булочку с маком."""
    d.ellipse((180, 330, 820, 780), fill="#d9923b")
    d.ellipse((260, 380, 600, 560), fill="#e8ad5c")
    rnd = random.Random(1)
    for _ in range(45):
        x, y = rnd.randint(300, 700), rnd.randint(400, 620)
        d.ellipse((x, y, x + 14, y + 14), fill="#2b2b3a")


# ---------- Сборка картинок ----------


def scene(bg, items, size):
    """Компонирует финальное изображение из одного или нескольких рисунков.

    Args:
        bg: цвет фона (hex-строка).
        items: список кортежей (рисунок, масштаб, x, y).
        size: итоговый размер (пиксели, квадрат).
    """
    img = Image.new("RGBA", (1000, 1000), bg)
    for motif, scale, x, y in items:
        layer = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
        motif(ImageDraw.Draw(layer))
        s = int(1000 * scale)
        img.alpha_composite(layer.resize((s, s), Image.LANCZOS), (x, y))
    return img.convert("RGB").resize((size, size), Image.LANCZOS)


def one(motif):
    """Возвращает список из одного элемента для scene() — утилита."""
    return [(motif, 1, 0, 0)]


# Варианты хлеба с разными цветами (через partial — подстановка параметров)
gouda = cheese
russian = partial(cheese, front="#f2e3a0", top="#f8efc4", side="#d8c77a")
white_bread = loaf
rye_bread = partial(loaf, body="#6b4423", slash="#a07040")

# путь: (фон, [(рисунок, масштаб, x, y)], размер)
IMAGES = {
    "categories/molochnye-produkty.jpg": (
        "#dff1f7",
        [(milk, 0.65, 50, 250), (cheese, 0.55, 400, 400)],
        600,
    ),
    "categories/ovoshchi-i-frukty.jpg": (
        "#e6f4d9",
        [(tomato, 0.6, 30, 300), (apple, 0.6, 370, 300)],
        600,
    ),
    "categories/hleb-i-vypechka.jpg": (
        "#fbeed6",
        [(white_bread, 0.65, 30, 300), (croissant, 0.55, 420, 350)],
        600,
    ),
    "subcategories/syry.jpg": ("#fff6d6", one(cheese), 600),
    "subcategories/moloko-i-kefir.jpg": ("#dff1f7", one(milk), 600),
    "subcategories/ovoshchi.jpg": ("#e6f4d9", one(tomato), 600),
    "subcategories/frukty.jpg": ("#fde8e8", one(apple), 600),
    "subcategories/hleb.jpg": ("#fbeed6", one(white_bread), 600),
    "subcategories/vypechka.jpg": ("#fdf0dc", one(croissant), 600),
    "products/syr-gauda.jpg": ("#fff6d6", one(gouda), 1200),
    "products/syr-rossiyskiy.jpg": ("#fbf6e3", one(russian), 1200),
    "products/moloko-3-2.jpg": ("#dff1f7", one(milk), 1200),
    "products/kefir-1.jpg": ("#e4f3ea", one(kefir), 1200),
    "products/pomidory.jpg": ("#fde8e8", one(tomato), 1200),
    "products/ogurtsy.jpg": ("#e6f4d9", one(cucumber), 1200),
    "products/yabloki.jpg": ("#fdeedd", one(apple), 1200),
    "products/banany.jpg": ("#fff9dc", one(banana), 1200),
    "products/hleb-belyy.jpg": ("#fbeed6", one(white_bread), 1200),
    "products/hleb-rzhanoy.jpg": ("#efe3d3", one(rye_bread), 1200),
    "products/kruassan.jpg": ("#fdf0dc", one(croissant), 1200),
    "products/bulochka-s-makom.jpg": ("#f6ead9", one(bun), 1200),
}

for rel_path, (bg, items, size) in IMAGES.items():
    full = os.path.join(MEDIA, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    scene(bg, items, size).save(full, quality=92)
    print("Создано:", full)

print(f"Готово: {len(IMAGES)} файлов")

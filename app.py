import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import os

CSV_FILE = 'Book5.xlsx - Sheet1.csv'
OUTPUT_DIR = 'generated_ads_card_style'
WIDTH, HEIGHT = 1080, 1080
BRAND_COLOR = "#0066FF"
BUTTON_COLOR = "#0066FF"
TEXT_COLOR_MAIN = "#FFFFFF"
TEXT_COLOR_DIM = "#CFCFCF"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_font(style, size):
    font_paths = {
        'bold': [
            '/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/System/Library/Fonts/Helvetica.ttc',
            'C:\\Windows\\Fonts\\arialbd.ttf',
        ],
        'regular': [
            '/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/System/Library/Fonts/Helvetica.ttc',
            'C:\\Windows\\Fonts\\arial.ttf',
        ]
    }
    for path in font_paths.get(style, font_paths['regular']):
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

def download_and_crop_image(url, target_size):
    try:
        if pd.isna(url) or not url:
            return Image.new('RGB', target_size, color="#666")
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content)).convert("RGB")
        target_ratio = target_size[0] / target_size[1]
        img_ratio = img.width / img.height
        if img_ratio > target_ratio:
            new_height = target_size[1]
            new_width = int(new_height * img_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            left = (new_width - target_size[0]) // 2
            img = img.crop((left, 0, left + target_size[0], target_size[1]))
        else:
            new_width = target_size[0]
            new_height = int(new_width / img_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            top = (new_height - target_size[1]) // 2
            img = img.crop((0, top, target_size[0], top + target_size[1]))
        return img
    except Exception as e:
        print(f"  ⚠ Image error: {e}")
        return Image.new('RGB', target_size, color="#666")

def add_gradient_overlay(img):
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    start_y = int(HEIGHT * 0.4)
    for y in range(start_y, HEIGHT):
        progress = (y - start_y) / (HEIGHT - start_y)
        alpha = int(220 * progress)
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

def draw_location_pin(draw, x, y, size, fill):
    r = size // 3
    cx = x + r
    cy = y + r
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    tail = [(cx - r, cy), (cx + r, cy), (cx, cy + size - r)]
    draw.polygon(tail, fill=fill)

def draw_ui(row):
    img_url = row.get('image[0].url')
    img = download_and_crop_image(img_url, (WIDTH, HEIGHT))
    img = add_gradient_overlay(img)
    draw = ImageDraw.Draw(img)
    font_brand = load_font('bold', 28)
    font_btn = load_font('bold', 20)
    font_label = load_font('regular', 16)
    font_value = load_font('bold', 22)
    font_loc = load_font('regular', 20)
    font_type = load_font('bold', 20)
    font_title = load_font('bold', 42)

    brand_text = "99acres.com"
    bbox = draw.textbbox((0, 0), brand_text, font=font_brand)
    brand_w = bbox[2] - bbox[0]
    draw.text((WIDTH - brand_w - 40, 35), brand_text, font=font_brand, fill=BRAND_COLOR)

    padding = 50
    current_y = HEIGHT - padding

    btn_text = "KNOW MORE"
    bbox = draw.textbbox((0, 0), btn_text, font=font_btn)
    btn_text_w = bbox[2] - bbox[0]
    btn_text_h = bbox[3] - bbox[1]
    btn_padding_x = 25
    btn_padding_y = 12
    btn_w = btn_text_w + btn_padding_x * 2
    btn_h = btn_text_h + btn_padding_y * 2
    btn_x = WIDTH - btn_w - padding
    btn_y = current_y - btn_h
    draw.rounded_rectangle([(int(btn_x), int(btn_y)), (int(btn_x + btn_w), int(btn_y + btn_h))], radius=6, fill=BUTTON_COLOR)
    draw.text((int(btn_x + btn_padding_x), int(btn_y + btn_padding_y)), btn_text, font=font_btn, fill=TEXT_COLOR_MAIN)
    current_y = btn_y - 35

    info_bar_height = 70
    info_bar_y = current_y - info_bar_height

    price_label = str(row.get('price_label', ''))
    price_text = price_label.replace('onwards', '').strip() if price_label and price_label != 'nan' else "Price on Request"

    draw.text((padding, info_bar_y), "Price", font=font_label, fill=TEXT_COLOR_DIM)
    draw.text((padding, info_bar_y + 25), price_text, font=font_value, fill=TEXT_COLOR_MAIN)

    area = str(row.get('area', ''))
    if area and area != 'nan':
        area_text = area
    else:
        config_area = row.get('configurations[0].area', '')
        area_text = str(config_area) if pd.notna(config_area) else "Contact"

    carpet_x = padding + 250
    draw.text((carpet_x, info_bar_y), "Carpet Area", font=font_label, fill=TEXT_COLOR_DIM)
    draw.text((carpet_x, info_bar_y + 25), area_text, font=font_value, fill=TEXT_COLOR_MAIN)

    current_y = info_bar_y - 30

    locality = str(row.get('locality', '')).strip()
    city = str(row.get('city', '')).strip()
    if locality and locality.lower() != 'nan' and city and city.lower() != 'nan':
        loc_text = f"{locality}, {city}"
    elif city and city.lower() != 'nan':
        loc_text = city
    elif locality and locality.lower() != 'nan':
        loc_text = locality
    else:
        loc_text = "Prime Location"

    pin_size = 20
    loc_x = padding
    loc_y = current_y - pin_size - 4
    draw_location_pin(draw, int(loc_x), int(loc_y), pin_size, fill=BUTTON_COLOR)
    draw.text((loc_x + pin_size + 10, loc_y), loc_text, font=font_loc, fill=TEXT_COLOR_DIM)
    current_y -= (pin_size + 20)

    property_type = str(row.get('property_type', 'Apartment')).upper()
    config_name = str(row.get('configurations[0].name', '')).upper().strip()
    type_text = f"{config_name} {property_type}" if config_name and config_name != 'NAN' else property_type
    bbox = draw.textbbox((0, 0), type_text, font=font_type)
    type_h = bbox[3] - bbox[1]
    draw.text((padding, current_y - type_h), type_text, font=font_type, fill=TEXT_COLOR_MAIN)
    current_y -= (type_h + 15)

    title = str(row.get('property_title', 'LUXURY PROPERTY')).upper()
    words = title.split()
    lines = []
    current_line = []
    max_width = WIDTH - padding * 2
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font_title)
        if bbox[2] - bbox[0] < max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    for line in reversed(lines):
        bbox = draw.textbbox((0, 0), line, font=font_title)
        line_h = bbox[3] - bbox[1]
        draw.text((padding, current_y - line_h), line, font=font_title, fill=TEXT_COLOR_MAIN)
        current_y -= (line_h + 8)

    p_id = str(row.get('property_ID', 'idx')).replace('/', '_')
    file_name = f"{OUTPUT_DIR}/ad_{p_id}.jpg"
    img.save(file_name, quality=95)
    print(f"  ✓ {file_name}")

if __name__ == "__main__":
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        print(f"\nGenerating {len(df)} card-style ads...\n")
        for index, row in df.iterrows():
            try:
                draw_ui(row)
            except Exception as e:
                print(f"  ✗ Row {index}: {e}")
        print(f"\nComplete! Check '{OUTPUT_DIR}' folder\n")
    else:
        print(f"Error: CSV file not found.")

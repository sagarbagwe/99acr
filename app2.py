import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import os

CSV_FILE = 'Book5.xlsx - Sheet1.csv'
OUTPUT_DIR = 'generated_ads_card_style_4'
WIDTH, HEIGHT = 1080, 1080
BRAND_COLOR = "#0066FF"
BUTTON_COLOR = "#0066FF"
TEXT_COLOR_MAIN = "#FFFFFF"
TEXT_COLOR_DIM = "#CFCFCF"
TOP_BIAS = 0.18

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_font(style, size):
    font_paths = {
        'bold': [
            'Roboto-Bold.ttf',
            '/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            'C:\\Windows\\Fonts\\arialbd.ttf',
        ],
        'regular': [
            'Roboto-Regular.ttf',
            '/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            'C:\\Windows\\Fonts\\arial.ttf',
        ]
    }
    for p in font_paths.get(style, font_paths['regular']):
        try:
            return ImageFont.truetype(p, size)
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
            top_extra = new_height - target_size[1]
            top = int(top_extra * TOP_BIAS)
            img = img.crop((0, top, target_size[0], top + target_size[1]))
        return img
    except Exception as e:
        print("  ⚠ Image error:", e)
        return Image.new('RGB', target_size, color="#666")

def add_gradient_overlay(img):
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    start_y = int(HEIGHT * 0.40)
    for y in range(start_y, HEIGHT):
        p = (y-start_y)/(HEIGHT-start_y)
        a = int(245 * p)
        d.line([(0,y),(WIDTH,y)], fill=(0,0,0,a))
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

def draw_location_pin(draw, x, y, size, fill):
    r = size // 3
    cx = x + r
    cy = y + r
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)
    draw.polygon([(cx-r, cy), (cx+r, cy), (cx, cy+size-r)], fill=fill)

def draw_ui(row):
    img_url = row.get('image[0].url')
    img = download_and_crop_image(img_url, (WIDTH, HEIGHT))
    img = add_gradient_overlay(img)
    draw = ImageDraw.Draw(img)

    font_brand = load_font('bold', 36)
    font_title = load_font('bold', 64)
    font_type = load_font('bold', 24)
    font_loc = load_font('regular', 26)
    font_label = load_font('regular', 24)  # increased label size
    font_value = load_font('bold', 38)     # increased value size
    font_btn = load_font('bold', 24)

    brand = "99acres.com"
    bw = draw.textbbox((0,0), brand, font=font_brand)[2]
    draw.text((WIDTH - bw - 44, 38), brand, font=font_brand, fill=BRAND_COLOR)

    padding = 56
    current_y = HEIGHT - padding

    btn_text = "KNOW MORE"
    btn_w = 240
    btn_h = 62
    btn_x = WIDTH - btn_w - padding
    btn_y = current_y - btn_h
    draw.rounded_rectangle([(btn_x, btn_y),(btn_x+btn_w, btn_y+btn_h)], radius=10, fill=BUTTON_COLOR)
    tbw = draw.textbbox((0,0), btn_text, font=font_btn)[2]
    text_x = btn_x + (btn_w - tbw)/2
    draw.text((int(text_x), int(btn_y + (btn_h - font_btn.size)/2 - 2)), btn_text, font=font_btn, fill=TEXT_COLOR_MAIN)
    current_y = btn_y - 40

    line_y = current_y - 10
    rule_margin = padding
    draw.line([(rule_margin, line_y), (WIDTH - rule_margin, line_y)], fill=BRAND_COLOR, width=3)
    current_y = line_y - 24

    price_label = str(row.get('price_label',''))
    price = price_label.replace('onwards','').strip() if price_label and price_label != 'nan' else "Price on Request"
    draw.text((padding, current_y - 6), "Price", font=font_label, fill=TEXT_COLOR_DIM)
    draw.text((padding, current_y + 36), price, font=font_value, fill=TEXT_COLOR_MAIN)

    carpet_x = padding + 360
    area = str(row.get('area',''))
    if area and area.lower()!='nan':
        area_text = area
    else:
        config_area = row.get('configurations[0].area','')
        area_text = str(config_area) if pd.notna(config_area) and config_area!='' else "Contact"
    draw.text((carpet_x, current_y - 6), "Carpet Area", font=font_label, fill=TEXT_COLOR_DIM)
    draw.text((carpet_x, current_y + 36), area_text, font=font_value, fill=TEXT_COLOR_MAIN)

    current_y = current_y - 48

    locality = str(row.get('locality','')).strip()
    city = str(row.get('city','')).strip()
    if locality and locality.lower()!='nan' and city and city.lower()!='nan':
        loc_text = f"{locality}, {city}"
    elif city and city.lower()!='nan':
        loc_text = city
    elif locality and locality.lower()!='nan':
        loc_text = locality
    else:
        loc_text = "Prime Location"

    pin_size = 26
    loc_x = padding
    loc_y = current_y - pin_size - 2
    draw_location_pin(draw, int(loc_x), int(loc_y), pin_size, fill=BUTTON_COLOR)
    draw.text((loc_x + pin_size + 12, loc_y - 2), loc_text, font=font_loc, fill=TEXT_COLOR_DIM)
    current_y = loc_y - 32

    property_type = str(row.get('property_type','Apartment')).upper()
    config_name = str(row.get('configurations[0].name','')).upper().strip()
    type_text = f"{config_name} {property_type}" if config_name and config_name!='NAN' else property_type
    draw.text((padding, current_y), type_text, font=font_type, fill=TEXT_COLOR_MAIN)
    current_y -= 46

    title = str(row.get('property_title','LUXURY PROPERTY')).upper()
    max_w = WIDTH - padding*2 - 20
    words = title.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0,0), test, font=font_title)[2] <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    lines = lines[:3]
    ty = current_y
    for ln in reversed(lines):
        bbox = draw.textbbox((0,0), ln, font=font_title)
        h = bbox[3] - bbox[1]
        draw.text((padding, ty - h), ln, font=font_title, fill=TEXT_COLOR_MAIN)
        ty -= (h + 8)

    p_id = str(row.get('property_ID','idx')).replace('/','_')
    out = os.path.join(OUTPUT_DIR, f"ad_{p_id}.png")
    img.save(out, format='PNG')
    print("✓", out)

if __name__ == "__main__":
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        print(f"Generating {len(df)} images...")
        for i, r in df.iterrows():
            try:
                draw_ui(r)
            except Exception as e:
                print("✗", i, e)
    else:
        print("CSV not found")

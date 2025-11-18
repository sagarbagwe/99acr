
import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

# --- CONFIGURATION ---
CSV_FILE = 'Book5.xlsx - Sheet1.csv'
OUTPUT_DIR = 'generated_ads_clean_style'

# Canvas Settings
WIDTH, HEIGHT = 1080, 1080
BRAND_COLOR = "#004B8D"
BUTTON_COLOR = "#FFFFFF"
BUTTON_TEXT_COLOR = "#004B8D"
TEXT_COLOR_MAIN = "#FFFFFF"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_font(url, filename):
    """Download font file if it doesn't exist."""
    if not os.path.exists(filename):
        try:
            print(f"Downloading font: {filename}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✓ Font downloaded: {filename}")
        except Exception as e:
            print(f"✗ Could not download font: {e}")
            return False
    return True

# Download free fonts (Roboto from Google Fonts)
FONT_BOLD_PATH = "Roboto-Bold.ttf"
FONT_REGULAR_PATH = "Roboto-Regular.ttf"

# Download fonts if needed
download_font("https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf", FONT_BOLD_PATH)
download_font("https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf", FONT_REGULAR_PATH)

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def download_and_crop_image(url, target_size):
    """Downloads image and fills the entire target size (Center Crop)."""
    try:
        if pd.isna(url) or not url:
            return Image.new('RGB', target_size, color="#666")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")
        
        # Center crop to fill target size
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
        print(f"Error processing image: {e}")
        return Image.new('RGB', target_size, color="#666")

def add_bottom_overlay(img):
    """Adds a semi-transparent dark overlay only at the bottom 40%."""
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Start overlay from 60% down
    start_y = int(HEIGHT * 0.6)
    
    # Solid dark overlay at bottom
    draw.rectangle([(0, start_y), (WIDTH, HEIGHT)], fill=(0, 0, 0, 160))
    
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

def draw_top_ribbon(draw, text):
    """Draws a clean ribbon at top left corner."""
    ribbon_width = 260
    ribbon_height = 50
    
    # Draw rectangle
    draw.rectangle([(0, 0), (ribbon_width, ribbon_height)], fill=BRAND_COLOR)
    
    # Text
    font = load_font(FONT_BOLD_PATH, 22)
    bbox = draw.textbbox((0, 0), text.upper(), font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (ribbon_width - text_w) // 2
    text_y = (ribbon_height - text_h) // 2
    draw.text((text_x, text_y), text.upper(), font=font, fill=TEXT_COLOR_MAIN)

def draw_ui(row):
    # 1. Background Image (Full Canvas)
    img_url = row.get('image[0].url')
    img = download_and_crop_image(img_url, (WIDTH, HEIGHT))
    
    # 2. Add dark overlay at bottom only
    img = add_bottom_overlay(img)
    draw = ImageDraw.Draw(img)
    
    # --- TOP LEFT: Status Ribbon ---
    status = str(row.get('property_status', 'Ready To Move'))
    draw_top_ribbon(draw, status)
    
    # --- TOP RIGHT: Brand ---
    brand_text = "99acres.com"
    font_brand = load_font(FONT_BOLD_PATH, 32)
    bbox = draw.textbbox((0, 0), brand_text, font=font_brand)
    brand_w = bbox[2] - bbox[0]
    draw.text((WIDTH - brand_w - 30, 30), brand_text, font=font_brand, fill=TEXT_COLOR_MAIN)
    
    # --- BOTTOM SECTION (Clean & Minimal) ---
    
    # Start from bottom
    current_y = HEIGHT - 30
    
    # 1. T&C Text (Small, bottom right)
    tc_text = "* T&C APPLY"
    font_tc = load_font(FONT_REGULAR_PATH, 16)
    bbox = draw.textbbox((0, 0), tc_text, font=font_tc)
    tc_w = bbox[2] - bbox[0]
    tc_h = bbox[3] - bbox[1]
    draw.text((WIDTH - tc_w - 25, current_y - tc_h), tc_text, font=font_tc, fill="#999")
    current_y -= (tc_h + 25)
    
    # 2. "Enquire Now" Button (Centered, white)
    btn_w, btn_h = 300, 60
    btn_x = (WIDTH - btn_w) // 2
    btn_y = current_y - btn_h
    
    draw.rounded_rectangle([(btn_x, btn_y), (btn_x + btn_w, current_y)], 
                          radius=5, fill=BUTTON_COLOR)
    
    btn_text = "Enquire Now"
    font_btn = load_font(FONT_BOLD_PATH, 28)
    bbox = draw.textbbox((0, 0), btn_text, font=font_btn)
    btn_text_w = bbox[2] - bbox[0]
    btn_text_h = bbox[3] - bbox[1]
    draw.text((btn_x + (btn_w - btn_text_w) // 2, btn_y + (btn_h - btn_text_h) // 2), 
             btn_text, font=font_btn, fill=BUTTON_TEXT_COLOR)
    
    current_y = btn_y - 35
    
    # 3. Price Line
    price_label = str(row.get('price_label', 'Price on Request'))
    if price_label != 'nan' and price_label != 'Price on Request':
        price_text = f"PRICE STARTS AT ₹ {price_label}"
    else:
        price_text = "PRICE ON REQUEST"
    
    font_price = load_font(FONT_BOLD_PATH, 24)
    bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_w = bbox[2] - bbox[0]
    price_h = bbox[3] - bbox[1]
    draw.text(((WIDTH - price_w) // 2, current_y - price_h), 
             price_text, font=font_price, fill=TEXT_COLOR_MAIN)
    current_y -= (price_h + 12)
    
    # 4. Configuration Type
    config_name = str(row.get('configurations[0].name', '')).upper().strip()
    if config_name == 'NAN' or not config_name:
        config_name = "LUXURY"
    
    config_text = f"{config_name} APARTMENTS"
    font_config = load_font(FONT_REGULAR_PATH, 22)
    bbox = draw.textbbox((0, 0), config_text, font=font_config)
    config_w = bbox[2] - bbox[0]
    config_h = bbox[3] - bbox[1]
    draw.text(((WIDTH - config_w) // 2, current_y - config_h), 
             config_text, font=font_config, fill=TEXT_COLOR_MAIN)
    current_y -= (config_h + 25)
    
    # 5. Location (with subtle text)
    locality = str(row.get('locality', ''))
    city = str(row.get('city', ''))
    
    if locality != 'nan' and city != 'nan':
        loc_text = f"{locality}, {city}"
    elif city != 'nan':
        loc_text = city
    else:
        loc_text = "Prime Location"
    
    font_loc = load_font(FONT_REGULAR_PATH, 20)
    bbox = draw.textbbox((0, 0), loc_text, font=font_loc)
    loc_w = bbox[2] - bbox[0]
    loc_h = bbox[3] - bbox[1]
    draw.text(((WIDTH - loc_w) // 2, current_y - loc_h), 
             loc_text, font=font_loc, fill="#CCC")
    current_y -= (loc_h + 18)
    
    # 6. Property Title (Large, Bold, Centered)
    title = str(row.get('property_title', 'LUXURY APARTMENTS')).upper()
    font_title = load_font(FONT_BOLD_PATH, 52)
    
    # Simple word wrapping
    words = title.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font_title)
        if bbox[2] - bbox[0] < WIDTH - 120:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw title lines (from bottom up)
    for line in reversed(lines):
        bbox = draw.textbbox((0, 0), line, font=font_title)
        line_w = bbox[2] - bbox[0]
        line_h = bbox[3] - bbox[1]
        draw.text(((WIDTH - line_w) // 2, current_y - line_h), 
                 line, font=font_title, fill=TEXT_COLOR_MAIN)
        current_y -= (line_h + 8)
    
    # --- SAVE ---
    p_id = str(row.get('property_ID', 'idx')).replace('/', '_')
    file_name = f"{OUTPUT_DIR}/ad_{p_id}.jpg"
    img.save(file_name, quality=92)
    print(f"✓ Generated: {file_name}")

# --- MAIN ---
if __name__ == "__main__":
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        print(f"\nFound {len(df)} properties. Generating clean ads...\n")
        for index, row in df.iterrows():
            try:
                draw_ui(row)
            except Exception as e:
                print(f"✗ Failed on row {index}: {e}")
        print(f"\n✓ Complete! Check '{OUTPUT_DIR}' folder\n")
    else:
        print(f"Error: CSV file not found.")

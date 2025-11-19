Real Estate Ad Generator

A Python automation tool that generates professional, social-media-ready real estate advertisement images in bulk. It reads property data from a CSV file, downloads listing images, and overlays branded text, pricing, and call-to-action buttons, mimicking high-quality design standards.

🌟 Features

Bulk Generation: Process hundreds of property listings from a single CSV file in seconds.

Smart Image Handling: Automatically downloads, centers, and crops images to fit a 1080x1080 (1:1) social media aspect ratio without distortion.

Dynamic Text Overlay: Automatically overlays property titles, locations, prices, and amenities.

Professional Aesthetics:

Gradient Overlays: Adds dynamic gradients to ensure text is readable against any background.

Branded Ribbons: Generates "Under Construction" or status ribbons dynamically.

Modern UI: Includes CTA buttons ("Enquire Now") and clean typography.

Robust Error Handling: Skips corrupt images or missing data without crashing the batch process.

🛠️ Prerequisites

You need Python 3.7+ installed on your system.

Required Libraries

Install the necessary Python packages using the provided requirements file:

pip install -r requirements.txt


📂 Project Structure

project-folder/
│
├── ad_generator.py       # The main Python script
├── Book5.xlsx - Sheet1.csv  # Input data file (your CSV)
├── requirements.txt      # List of dependencies
├── arial.ttf             # Regular font file (optional, defaults to system)
├── arialbd.ttf           # Bold font file (optional, defaults to system)
│
└── generated_ads_refined/ # Output folder (created automatically)
    ├── ad_refined_101.jpg
    ├── ad_refined_102.jpg
    └── ...


🚀 Usage

Prepare your CSV file: Ensure your data matches the expected column headers (see CSV Data Structure below).

Place Font Files: (Optional) For the best look, place arial.ttf and arialbd.ttf in the same folder as the script. If missing, the script will try to use default system fonts.

Run the Script:

python ad_generator.py


Check Output: The generated images will appear in the generated_ads_refined folder.

📊 CSV Data Structure

The script expects a CSV file (configured as CSV_FILE in the code) with the following columns:

Column Header

Description

Example

property_ID

Unique identifier for the generated filename

R424460

image[0].url

Direct URL to the main property image

https://example.com/img.jpg

property_title

Main title of the property

Luxury Apartments

possession_status

Text for the top-left ribbon

Under Construction

locality

Neighborhood name

Nanakramguda

city

City name

Hyderabad

configurations[0].name

Type of unit

3 BHK Apartment

price_label

Starting price

1.5 Cr

price_max_label

(Optional) Max price for range

2.1 Cr

⚙️ Configuration

You can adjust the settings at the top of the ad_generator.py file:

# --- CONFIGURATION ---
CSV_FILE = 'Book5.xlsx - Sheet1.csv'  # Path to your input CSV
OUTPUT_DIR = 'generated_ads_refined'  # Folder where images are saved

# Canvas Dimensions
WIDTH, HEIGHT = 1080, 1080

# Colors (Hex Codes)
BRAND_COLOR = "#004B8D"      # Blue for Ribbon/Brand
BUTTON_COLOR = "#FFFFFF"     # White for Buttons
BUTTON_TEXT_COLOR = "#004B8D" # Text inside buttons


🎨 Customization

Fonts: To use custom fonts (like Roboto or OpenSans), download the .ttf files, place them in the project folder, and update FONT_BOLD_PATH and FONT_REGULAR_PATH in the script.

Brand Logo: Currently, the script types "99acres.com" as text. You can modify the draw_ui function to img.paste() a logo image instead if required.

📝 Notes

Internet Access: The script requires an active internet connection to download images from the URLs provided in the CSV.

Image Quality: The output quality depends on the resolution of the source images in your CSV. High-res inputs yield the best results.

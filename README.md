
# 🏡 Real Estate Auto Ad Generator

### **Automated Property Image Card Creator (99acres-style)**

This tool automatically generates high-quality real estate advertisement cards using Python, PIL, and CSV/Excel property data.
The output images match the **99acres style**, including:

✔ Gradient overlay
✔ Big bold title
✔ Location pin
✔ Price & Carpet Area layout
✔ Blue vertical divider between Price and Carpet Area
✔ CTA button (“Know More”)
✔ Auto-cropped property photos

---

## 📌 Features

### ✅ **Generate Ads From CSV**

Reads property details (title, location, price, area, image URL, etc.) and auto-creates ads.

### ✅ **99acres-Styled Design**

* Full-screen image with bottom dark gradient
* Large white property title
* Location with custom-drawn blue pin
* Price & Carpet Area in two columns
* **Vertical blue rounded divider** between Price & Area
* Horizontal top separator line
* "Know More" button (blue CTA)
* Blue 99acres branding on top-right

### ✅ **Smart Image Cropping**

Automatically center-crops each property image with **TOP_BIAS** to preserve the important content.

### ✅ **High-Quality Output**

* PNG images (lossless)
* Anti-aliased fonts
* Smooth rounded shapes and dividers

---

## 📂 Folder Structure

```
project/
│
├── app.py               # Main generator script
├── Book5.xlsx - Sheet1.csv   # Input data file
├── generated_ads_card/       # Output PNG images
└── README.md                 # Documentation
```

---

## 📥 Input CSV Format

Your input CSV should contain these columns:

| Column Name              | Description                                   |
| ------------------------ | --------------------------------------------- |
| `property_ID`            | Unique ID for saving output files             |
| `property_title`         | Display name of the property                  |
| `locality`               | Area / locality                               |
| `city`                   | City name                                     |
| `price_label`            | Price string (e.g., "₹ 78 Lacs")              |
| `area`                   | Carpet area (e.g., "1800 sq.ft.")             |
| `configurations[0].name` | Property type (e.g., 2BHK, INDEPENDENT HOUSE) |
| `configurations[0].area` | Fallback if area missing                      |
| `image[0].url`           | Property Image URL                            |

---

## ▶️ How To Run

### **1. Install Required Libraries**

```bash
pip install pillow pandas requests
```

### **2. Place Your CSV File**

Name your CSV:

```
Book5.xlsx - Sheet1.csv
```

(or update the filename inside script)

### **3. Run the Script**

```bash
python app.py
```

### **4. Output Images**

All generated images will appear in:

```
generated_ads_card/
```

Each file is automatically named:

```
ad_<property_ID>.png
```

---

## 🎨 Appearance Matching 99acres Style

The script includes:

### **Gradient Overlay**

Improves text readability.

### **Font Styling**

* Titles: bold, large (64px)
* Labels: medium (24px)
* Values: large (38px)

### **Blue Divider (Exact Match)**

Vertical blue rounded divider:

```
Price  |  Carpet Area
```

### **Full-Width Blue Line**

Thin blue line above the price bar.

### **CTA Button**

Rounded blue button:

```
[ KNOW MORE ]
```

---

## ⚙️ Configuration Options

Inside the script:

### ⭐ **TOP_BIAS**

Adjusts how much of the top part of image is preserved.

```python
TOP_BIAS = 0.18
```

Increase to see more ceiling
Decrease to see more floor

---

## 🖼 Example Output

(Image similar to your sample 99acres card)

✔ Full image background
✔ Bottom dark fade
✔ Big white title
✔ Blue pin
✔ Price + Carpet Area divider
✔ Blue CTA

---

## 🧩 Troubleshooting

### ❗ Font not loading

Add `Roboto-Bold.ttf` and `Roboto-Regular.ttf` in project root.

### ❗ Image looks too dark

Reduce gradient strength in:

```python
add_gradient_overlay()
```

### ❗ Image cropping wrong

Adjust:

```python
TOP_BIAS = 0.18
```

---

If you want, I can also generate an **example CSV**, **sample output**, or a **GitHub README badge version**.

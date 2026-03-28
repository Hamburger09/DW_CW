# ◈ DATA STUDIO

> A Streamlit-based data cleaning, transformation, and visualization application.

---

## What Is Data Studio?

Data Studio is a fully interactive, browser-based data processing app built with Streamlit and Python. It lets you upload raw datasets, clean and transform data without writing any code, build visualizations, and export the results — all in one place.

---

## Installation (Google Colab)

Run each command in a **separate cell**, one at a time:

```bash
!pip install streamlit
```
```bash
!pip install matplotlib
```
```bash
!pip install gspread google-auth
```
```bash
!pip install psycopg2-binary
```

---

## How to Run

### In Google Colab

**Cell 1** — Save the app file:
```
%%writefile app.py
# the code is given in google colab
```



**Cell 2** — Credentials:
```
%%writefile google_sheets.json
# the code is given in google colab
# The essential google service credentials so that the application could connect to Google sheets
```


**Cell 3** — Download Cloudfare:
```
!wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
!chmod +x cloudflared-linux-amd64
```


**Cell 4** — Launch:
```
!streamlit run app.py &>/dev/null &

import time
time.sleep(8)

!./cloudflared-linux-amd64 tunnel --url http://localhost:8501
# Command runs and outputs a link but sometimes it needs more time to execute and then the link will work and the application boots
```


A public URL like `Tunnel on trycloudflare.com...` will appear — open it in your browser.



## Features

### Tab 1 — Upload & Overview
Load data via the sidebar. Supported formats:
- CSV, Excel (.xlsx), JSON
- Google Sheets (paste URL + click **Load Google Sheet**)

Displays: row/column counts, data types, summary statistics, missing value report, and duplicate count.

### Tab 2 — Cleaning Studio

| Sub-tab | What it does |
|---|---|
| Missing Values | Drop rows/columns, fill with constant, mean/median/mode, forward/backward fill |
| Duplicates | Detect and remove duplicate rows (full or subset of columns) |
| Data Types | Convert columns to Numeric, Categorical, or Datetime |
| Categorical Tools | Trim/lowercase, title case, value mapping, rare category grouping, one-hot encoding |
| Numeric Cleaning | Detect and handle outliers via IQR or Z-score (remove or cap/Winsorize) |
| Scaling | Min-Max scaling or Z-score standardization |
| Column Operations | Rename, drop, create new columns from formulas, log/demean, binning |
| Data Validation | Range checks, allowed category lists, non-null constraints |

### Tab 3 — Visualization Builder
Build charts with optional filters. Chart types:
- Histogram, Box Plot, Scatter Plot, Line Chart, Bar Chart, Correlation Heatmap

### Tab 4 — Export & Report
Download your results:
- Cleaned dataset as **CSV** or **Excel**
- **Transformation Report** (CSV) — every step you applied
- **JSON Recipe** — replayable record of all transformations
- **Python Script** — auto-generated pipeline replay script

---

## Transformation Log & Undo

Every cleaning action is logged in the sidebar. Click **Undo Last Step** at any time to roll back the most recent transformation.

---


---

## File Structure

```
app.py                      # Main application 
google_sheets.json          # Optional: Google service account credentials
transformation_report.csv
sample_data/ 
   ecommerce.xlsx
   hr_employees.csv
AI_chat_prompts/
requirements.txt

```

---

## Reset

Click **Reset Session** in the sidebar to clear all data and start fresh.

## The deployed application link
https://rcwdbjnx8wbscc3jse7ygv.streamlit.app/
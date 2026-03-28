# Data Studio: AI-Assisted Data Wrangler
A professional Streamlit-based ETL (Extract, Transform, Load) application designed to automate data cleaning, profiling, and visualization.
## Key Features
### 1. Data Extraction
* **Multi-Source Upload:** Supports CSV and Excel files.
* **Cloud & DB Integration:** Direct connection to **Google Sheets** and **SQL Databases**.
### 2. Cleaning & Transformation Studio
* **Missing Data:** Tools to drop or impute null values.
* **Data Typing:** Fast conversion to Numeric, Categorical, or Datetime formats.
* **Advanced Processing:** Outlier handling, data scaling, and One-hot encoding.
* **Structural Edits:** Remove duplicates and drop unnecessary columns.
### 3. Analytics & Visualization
* **Exploratory Data Analysis (EDA):** Automated data profiling and summary statistics.
* **Visual Builder:** Custom chart generation (Histograms, Scatter plots, etc.) using Matplotlib.
### 4. Export & Pipeline Generation
* **Data Export:** Download cleaned datasets as CSV.
* **Pipeline Script:** Automatically generates a **Python script** that logs and reproduces every cleaning step performed in the UI.
## Tech Stack
* **Language:** Python 3.x
* **Framework:** Streamlit
* **Libraries:** Pandas, NumPy, Matplotlib, Gspread, SQLAlchemy
## Installation & Setup
1. Install dependencies:
   ```bash
   pip install streamlit pandas numpy matplotlib gspread sqlalchemy google-auth

import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Studio", layout="wide")
st.markdown("""
<style>

/* ── Root tokens ── */
:root {
    --bg:        #0f1117;
    --surface:   #1a1d27;
    --surface2:  #22263a;
    --border:    #2e3248;
    --accent:    #f0a500;
    --accent2:   #e05c2a;
    --text:      #e8eaf0;
    --muted:     #7a7f9a;
    --success:   #2ecc71;
    --danger:    #e74c3c;
    --radius:    10px;
}

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Custom app header ── */
[data-testid="stAppViewContainer"]::before {
    content: "◈ DATA STUDIO";
    display: block;
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4em;
    color: var(--accent);
    padding: 18px 2rem 0;
    text-transform: uppercase;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    font-family: 'DM Mono', monospace !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--accent) !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ── Main headings ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
}
h1 {
    font-size: 2rem !important;
    border-bottom: 2px solid var(--accent);
    padding-bottom: 0.4rem;
    margin-bottom: 1.5rem !important;
}
h2 { font-size: 1.3rem !important; color: var(--accent) !important; }
h3 { font-size: 1rem !important; color: var(--muted) !important; letter-spacing: 0.08em; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--surface) !important;
    border-radius: var(--radius) !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 2px !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    color: var(--muted) !important;
    background: transparent !important;
    border-radius: 6px !important;
    padding: 6px 16px !important;
    transition: all 0.2s ease !important;
    border: none !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--accent) !important;
    color: #0f1117 !important;
    font-weight: 500 !important;
}
[data-testid="stTabs"] [role="tab"]:hover:not([aria-selected="true"]) {
    color: var(--text) !important;
    background: var(--surface2) !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
    background: var(--surface2) !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: var(--radius) !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.18s ease !important;
}
[data-testid="stButton"] > button:hover {
    background: var(--accent) !important;
    color: #0f1117 !important;
}

/* ── Download buttons ── */
[data-testid="stDownloadButton"] > button {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    background: transparent !important;
    color: var(--accent2) !important;
    border: 1px solid var(--accent2) !important;
    border-radius: var(--radius) !important;
    width: 100% !important;
    transition: all 0.18s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: var(--accent2) !important;
    color: white !important;
}

/* ── Inputs, selects, text areas ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background-color: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(240,165,0,0.15) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface2) !important;
    border: 1px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

/* ── Dataframes / tables ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] * {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}

/* ── Metric / info / warning / success boxes ── */
[data-testid="stInfo"] {
    background: rgba(240,165,0,0.08) !important;
    border: 1px solid rgba(240,165,0,0.3) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}
[data-testid="stSuccess"] {
    background: rgba(46,204,113,0.08) !important;
    border: 1px solid rgba(46,204,113,0.3) !important;
    border-radius: var(--radius) !important;
}
[data-testid="stWarning"] {
    background: rgba(224,92,42,0.08) !important;
    border: 1px solid rgba(224,92,42,0.3) !important;
    border-radius: var(--radius) !important;
}
[data-testid="stError"] {
    background: rgba(231,76,60,0.08) !important;
    border: 1px solid rgba(231,76,60,0.35) !important;
    border-radius: var(--radius) !important;
}

/* ── Radio buttons ── */
[data-testid="stRadio"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    color: var(--text) !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] [role="slider"] {
    background: var(--accent) !important;
}
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: var(--muted) !important;
    font-size: 0.72rem !important;
}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    color: var(--text) !important;
}

/* ── Code blocks ── */
[data-testid="stCode"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}
code {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    color: var(--accent) !important;
}

/* ── Multiselect tags ── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: rgba(240,165,0,0.15) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 4px !important;
    color: var(--accent) !important;
    font-size: 0.72rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ── Section dividers ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 6.1  TRANSFORMATION LOG HELPERS
# ─────────────────────────────────────────────

def log_transformation(operation, parameters, affected_cols):
    """Append one entry to the transformation log and save a df snapshot for undo."""
    if "transformation_log" not in st.session_state:
        st.session_state["transformation_log"] = []
    if "df_snapshots" not in st.session_state:
        st.session_state["df_snapshots"] = []

    st.session_state["transformation_log"].append({
        "step": len(st.session_state["transformation_log"]) + 1,
        "operation": operation,
        "parameters": str(parameters),
        "affected_columns": str(affected_cols),
    })
    # snapshot BEFORE the change (current df)
    st.session_state["df_snapshots"].append(st.session_state["df"].copy())


# ─────────────────────────────────────────────
# 6.2  CACHED LOADERS & PROFILING
# ─────────────────────────────────────────────

@st.cache_data
def load_file(file_bytes, file_name):
    if file_name.endswith(".csv"):
        return pd.read_csv(file_bytes)
    elif file_name.endswith(".xlsx"):
        return pd.read_excel(file_bytes)
    elif file_name.endswith(".json"):
        return pd.read_json(file_bytes)
    return None


@st.cache_data
def load_google_sheet_service(url):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("google_sheets.json", scopes=scope)
    client = gspread.authorize(creds)

    try:
        sheet = client.open_by_url(url).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error: {e}")
        return None


@st.cache_data
def get_profile(df):
    missing = df.isnull().sum()
    return pd.DataFrame({
        "Column": df.columns,
        "Missing Count": missing.values,
        "Missing %": (missing / len(df) * 100).round(2).values
    })


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

st.sidebar.subheader("Load Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV / Excel / JSON",
    type=["csv", "xlsx", "json"],
    key="file_uploader"
)

st.sidebar.subheader("🔗 Google Sheets")
sheet_url = st.sidebar.text_input("Paste Google Sheets URL", key="sheet_url_input")
load_sheet_btn = st.sidebar.button("Load Google Sheet")

st.sidebar.title("Controls")

if st.sidebar.button("Reset Session"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ── Transformation Log in sidebar ──
st.sidebar.markdown("---")
st.sidebar.subheader("🕓 Transformation Log")

if "transformation_log" in st.session_state and st.session_state["transformation_log"]:
    log_df = pd.DataFrame(st.session_state["transformation_log"])
    st.sidebar.dataframe(log_df, use_container_width=True)

    if st.sidebar.button("↩️ Undo Last Step"):
        snapshots = st.session_state.get("df_snapshots", [])
        if snapshots:
            st.session_state["df"] = snapshots.pop().copy()
            st.session_state["df_snapshots"] = snapshots
            st.session_state["transformation_log"].pop()
            st.rerun()
        else:
            st.sidebar.warning("Nothing to undo.")
else:
    st.sidebar.info("No transformations yet.")


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────

tabs = st.tabs([
    "Upload & Overview",
    "Cleaning Studio",
    "Visualization Builder",
    "Export & Report"
])


# ══════════════════════════════════════════════
# TAB 0 – UPLOAD & OVERVIEW
# ══════════════════════════════════════════════

with tabs[0]:
    st.header("Upload & Overview")

    if uploaded_file is not None and "df" not in st.session_state:
        df = load_file(uploaded_file, uploaded_file.name)
        if df is not None:
            st.session_state["df"] = df

    if load_sheet_btn:
        if sheet_url:
            df = load_google_sheet_service(sheet_url)
            if df is not None and not df.empty:
                st.session_state["df"] = df
                st.success("Google Sheet loaded successfully ✅")
            else:
                st.error("Failed to load sheet")
        else:
            st.warning("Please paste a Google Sheets URL")

    if "df" in st.session_state:
        df = st.session_state["df"]

        st.subheader("Dataset Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"Rows: {df.shape[0]}")
        with col2:
            st.info(f"Columns: {df.shape[1]}")
        with col3:
            st.success(f"Total Columns: {df.shape[1]}")

        st.write("### Column Names")
        st.write(list(df.columns))

        st.subheader("Data Types")
        dtypes_df = df.dtypes.reset_index()
        dtypes_df.columns = ["Column", "Type"]
        st.dataframe(dtypes_df, use_container_width=True)

        st.subheader("Summary Statistics")
        st.write("#### Numeric Columns")
        if not df.select_dtypes(include="number").empty:
            st.dataframe(df.describe(), use_container_width=True)
        else:
            st.info("No numeric columns")

        st.write("#### Categorical Columns")
        if not df.select_dtypes(include=["object", "category"]).empty:
            st.dataframe(df.describe(include=["object", "category"]), use_container_width=True)
        else:
            st.info("No categorical columns")

        st.subheader("Missing Values")
        st.dataframe(get_profile(df), use_container_width=True)

        st.subheader("Duplicates")
        st.warning(f"Duplicate rows: {df.duplicated().sum()}")


# ══════════════════════════════════════════════
# TAB 1 – CLEANING STUDIO
# ══════════════════════════════════════════════

with tabs[1]:
    st.header("Cleaning & Preparation Studio")

    def highlight_changes(row):
        if row["Missing After"] < row["Missing Before"]:
            return ["background-color: #b3ffb3"] * 5
        return [""] * 5

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first on the Upload & Overview tab")
    else:
        df = st.session_state["df"]
        if "df_clean" not in st.session_state:
            st.session_state["df_clean"] = df.copy()

        cleaning_tabs = st.tabs([
            "Missing Values", "Duplicates", "Data Types",
            "Categorical Tools", "Numeric Cleaning",
            "Scaling / Normalization", "Column Operations", "Data Validation"
        ])

        # ── Missing Values ──────────────────────────────
        with cleaning_tabs[0]:
            df_clean = st.session_state["df_clean"]

            st.subheader("Missing Values Summary")
            missing = df_clean.isnull().sum()
            missing_percent = (missing / len(df_clean)) * 100
            missing_df = pd.DataFrame({
                "Column": df_clean.columns,
                "Missing Count": missing.values,
                "Missing %": missing_percent.values
            })
            st.dataframe(missing_df, use_container_width=True)

            st.subheader("Handle Missing Values")
            cols_with_missing = [col for col in df_clean.columns if df_clean[col].isnull().sum() > 0]

            if cols_with_missing:
                selected_cols = st.multiselect("Select columns to clean", cols_with_missing)
                action = st.radio("Select cleaning action", [
                    "Drop rows with missing values",
                    "Drop columns above missing threshold",
                    "Replace with constant",
                    "Replace with mean/median/mode",
                    "Forward fill / Backward fill"
                ])

                if selected_cols and action:
                    if st.button("Apply Cleaning"):
                        try:
                            before_missing = df_clean[selected_cols].isnull().sum()
                            before_missing_percent = (before_missing / len(df_clean) * 100).round(2)
                            df_clean = st.session_state["df_clean"]
                            before_rows, before_cols = df_clean.shape

                            if action == "Drop rows with missing values":
                                df_clean = df_clean.dropna(subset=selected_cols)

                            elif action == "Drop columns above missing threshold":
                                threshold = st.slider("Missing % threshold", 0, 100, 50, key="threshold_slider")
                                drop_cols = [col for col in selected_cols if df_clean[col].isnull().mean() * 100 > threshold]
                                df_clean = df_clean.drop(columns=drop_cols)
                                st.write(f"Dropped columns: {drop_cols}")

                            elif action == "Replace with constant":
                                const_value = st.text_input("Enter constant value", key="const_input")
                                if const_value != "":
                                    for col in selected_cols:
                                        df_clean[col] = df_clean[col].fillna(const_value)

                            elif action == "Replace with mean/median/mode":
                                for col in selected_cols:
                                    if pd.api.types.is_numeric_dtype(df_clean[col]):
                                        method = st.radio(f"Method for {col}", ["mean", "median", "mode"], key=f"method_{col}")
                                        if method == "mean":
                                            df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
                                        elif method == "median":
                                            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
                                        else:
                                            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
                                    else:
                                        df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

                            elif action == "Forward fill / Backward fill":
                                method = st.radio("Select method", ["forward", "backward"], key="ffill_bfill")
                                method_map = {"forward": "ffill", "backward": "bfill"}
                                df_clean[selected_cols] = df_clean[selected_cols].fillna(method=method_map[method])

                            after_rows, after_cols = df_clean.shape
                            st.session_state["df_clean"] = df_clean
                            st.session_state["df"] = df_clean
                            log_transformation(action, {}, selected_cols)

                            st.success(f"Cleaning applied ✅ Rows: {before_rows} → {after_rows}, Columns: {before_cols} → {after_cols}")

                            after_missing = df_clean[selected_cols].isnull().sum()
                            after_missing_percent = (after_missing / len(df_clean) * 100).round(2)

                            # guard: only show cols that still exist after drop
                            existing = [c for c in selected_cols if c in df_clean.columns]
                            if existing:
                                preview_df = pd.DataFrame({
                                    "Column": existing,
                                    "Missing Before": before_missing[existing].values,
                                    "Missing After": after_missing[existing].values,
                                    "Missing % Before": before_missing_percent[existing].values,
                                    "Missing % After": after_missing_percent[existing].values
                                })
                                st.subheader("Before / After Preview")
                                st.dataframe(preview_df.style.apply(highlight_changes, axis=1), use_container_width=True)
                        except Exception as e:
                            st.error(f"Cleaning failed: {e}")
            else:
                st.info("No missing values detected in this dataset.")

        # ── Duplicates ──────────────────────────────────
        with cleaning_tabs[1]:
            st.subheader("Duplicates Handling")
            df_clean = st.session_state["df"].copy()

            dup_type = st.radio("Detect duplicates by:", ["Full row", "Subset of columns"], key="dup_type")
            subset_cols = None
            if dup_type == "Subset of columns":
                subset_cols = st.multiselect("Select columns to check duplicates", df_clean.columns)

            duplicate_mask = df_clean.duplicated(subset=subset_cols, keep=False) if subset_cols else df_clean.duplicated(keep=False)
            dup_rows_before = duplicate_mask.sum()
            st.info(f"Duplicate rows detected: {dup_rows_before}")

            if dup_rows_before > 0 and st.checkbox("Show duplicate rows preview"):
                st.dataframe(df_clean[duplicate_mask], use_container_width=True)

            if dup_rows_before > 0:
                keep_option = st.radio("When removing duplicates, keep:", ["first", "last"], key="keep_option")
                if st.button("Remove Duplicates"):
                    try:
                        before_rows = df_clean.shape[0]
                        df_clean = df_clean.drop_duplicates(subset=subset_cols, keep=keep_option)
                        after_rows = df_clean.shape[0]
                        st.success(f"✅ Removed {before_rows - after_rows} duplicate rows! Rows: {before_rows} → {after_rows}")
                        st.session_state["df"] = df_clean
                        log_transformation("Remove Duplicates", {"keep": keep_option}, subset_cols or "all columns")
                        st.subheader("Preview of cleaned data")
                        st.dataframe(df_clean.head(), use_container_width=True)
                    except Exception as e:
                        st.error(f"Failed to remove duplicates: {e}")
            else:
                st.info("No duplicates detected.")

        # ── Data Types ──────────────────────────────────
        with cleaning_tabs[2]:
            st.subheader("Data Types & Parsing")
            df_clean = st.session_state["df"].copy()

            st.write("### Current Column Types")
            col_types = pd.DataFrame(df_clean.dtypes).reset_index()
            col_types.columns = ["Column", "Current Type"]
            st.dataframe(col_types, use_container_width=True)

            col_to_convert = st.selectbox("Select column to convert", df_clean.columns)
            if col_to_convert:
                st.write(f"Current type: `{df_clean[col_to_convert].dtype}`")
                new_type = st.radio("Convert to type:", ["Numeric", "Categorical", "Datetime"])

                if new_type == "Numeric":
                    remove_chars = st.text_input("Remove characters (e.g., $, ,)", value="$,")
                    if st.button("Convert to Numeric", key=f"convert_num_{col_to_convert}"):
                        try:
                            df_clean[col_to_convert] = df_clean[col_to_convert].astype(str)
                            for ch in remove_chars:
                                df_clean[col_to_convert] = df_clean[col_to_convert].str.replace(ch, "", regex=False)
                            df_clean[col_to_convert] = pd.to_numeric(df_clean[col_to_convert], errors="coerce")
                            st.success(f"Column '{col_to_convert}' converted to numeric!")
                            st.session_state["df"] = df_clean
                            log_transformation("Convert to Numeric", {"removed_chars": remove_chars}, [col_to_convert])
                            st.dataframe(df_clean[[col_to_convert]].head(), use_container_width=True)
                        except Exception as e:
                            st.error(f"Conversion failed: {e}")

                elif new_type == "Categorical":
                    if st.button("Convert to Categorical", key=f"convert_cat_{col_to_convert}"):
                        try:
                            df_clean[col_to_convert] = df_clean[col_to_convert].astype("category")
                            st.success(f"Column '{col_to_convert}' converted to categorical!")
                            st.session_state["df"] = df_clean
                            log_transformation("Convert to Categorical", {}, [col_to_convert])
                            st.dataframe(df_clean[[col_to_convert]].head(), use_container_width=True)
                        except Exception as e:
                            st.error(f"Conversion failed: {e}")

                elif new_type == "Datetime":
                    parse_format = st.text_input("Datetime format (leave blank for auto)", value="")
                    if st.button("Convert to Datetime", key=f"convert_dt_{col_to_convert}"):
                        try:
                            if parse_format.strip() == "":
                                df_clean[col_to_convert] = pd.to_datetime(df_clean[col_to_convert], errors="coerce")
                            else:
                                df_clean[col_to_convert] = pd.to_datetime(df_clean[col_to_convert], format=parse_format, errors="coerce")
                            st.success(f"Column '{col_to_convert}' converted to datetime!")
                            st.session_state["df"] = df_clean
                            log_transformation("Convert to Datetime", {"format": parse_format or "auto"}, [col_to_convert])
                            st.dataframe(df_clean[[col_to_convert]].head(), use_container_width=True)
                        except Exception as e:
                            st.error(f"Conversion failed: {e}")

        # ── Categorical Tools ───────────────────────────
        with cleaning_tabs[3]:
            st.subheader("Categorical Data Tools")
            df_clean = st.session_state["df"].copy()
            cat_cols = df_clean.select_dtypes(include=["object", "category"]).columns.tolist()

            if not cat_cols:
                st.info("No categorical columns detected in the dataset.")
            else:
                col = st.selectbox("Select categorical column to process", cat_cols)
                if col:
                    st.write(f"Unique values ({df_clean[col].nunique()}): {df_clean[col].dropna().unique()}")

                    st.write("### Standardize Values")
                    if st.button("Trim Whitespace & Lowercase", key=f"standardize_{col}"):
                        try:
                            df_clean[col] = df_clean[col].str.strip().str.lower()
                            st.success("✅ Values standardized (trimmed & lowercased)")
                            st.session_state["df"] = df_clean
                            log_transformation("Standardize: Trim & Lowercase", {}, [col])
                            st.dataframe(df_clean[[col]].head(10), use_container_width=True)
                        except Exception as e:
                            st.error(f"Error: {e}")

                    if st.button("Title Case", key=f"titlecase_{col}"):
                        try:
                            df_clean[col] = df_clean[col].str.title()
                            st.success("✅ Values converted to title case")
                            st.session_state["df"] = df_clean
                            log_transformation("Standardize: Title Case", {}, [col])
                            st.dataframe(df_clean[[col]].head(10), use_container_width=True)
                        except Exception as e:
                            st.error(f"Error: {e}")

                    st.write("### Mapping / Replacement")
                    st.info("Fill in the table below with original → new value pairs.")
                    mapping_rows = st.data_editor(
                        pd.DataFrame({"Original Value": [""], "New Value": [""]}),
                        num_rows="dynamic",
                        use_container_width=True,
                        key=f"mapping_editor_{col}"
                    )
                    set_other = st.checkbox("Set unmatched values to 'Other'?", key=f"set_other_{col}")

                    if st.button("Apply Mapping", key=f"apply_map_{col}"):
                        try:
                            mapping_dict = dict(zip(
                                mapping_rows["Original Value"],
                                mapping_rows["New Value"]
                            ))
                            mapping_dict = {k: v for k, v in mapping_dict.items() if str(k).strip() and str(v).strip()}
                            if not mapping_dict:
                                st.warning("Enter at least one mapping row.")
                            else:
                                mapped = df_clean[col].map(mapping_dict)
                                df_clean[col] = mapped.fillna("Other" if set_other else df_clean[col])
                                st.success("✅ Mapping applied!")
                                st.session_state["df"] = df_clean
                                log_transformation("Mapping / Replacement", {"mapping": mapping_dict, "set_other": set_other}, [col])
                                st.dataframe(df_clean[[col]].head(10), use_container_width=True)
                        except Exception as e:
                            st.error(f"Invalid mapping: {e}")

                    st.write("### Rare Category Grouping")
                    freq_threshold = st.slider("Frequency threshold (%)", 0, 100, 5)
                    if st.button("Group Rare Categories", key=f"rare_{col}"):
                        try:
                            counts = df_clean[col].value_counts(normalize=True) * 100
                            rare_values = counts[counts < freq_threshold].index
                            df_clean[col] = df_clean[col].replace(rare_values, "Other")
                            st.success(f"✅ {len(rare_values)} rare categories grouped into 'Other'")
                            st.session_state["df"] = df_clean
                            log_transformation("Rare Category Grouping", {"threshold_%": freq_threshold}, [col])
                            st.dataframe(df_clean[[col]].head(10), use_container_width=True)
                        except Exception as e:
                            st.error(f"Error: {e}")

                    st.write("### One-hot Encoding (Optional)")
                    if st.button("One-hot Encode Column", key=f"ohe_{col}"):
                        try:
                            df_clean = pd.get_dummies(df_clean, columns=[col], prefix=[col])
                            st.success("✅ One-hot encoding applied")
                            st.session_state["df"] = df_clean
                            log_transformation("One-hot Encoding", {}, [col])
                            st.dataframe(df_clean.head(10), use_container_width=True)
                        except Exception as e:
                            st.error(f"Error: {e}")

        # ── Numeric Cleaning ────────────────────────────
        with cleaning_tabs[4]:
            st.subheader("Numeric Cleaning & Outlier Handling")
            df_clean = st.session_state["df"].copy()
            num_cols = df_clean.select_dtypes(include="number").columns.tolist()

            if not num_cols:
                st.info("No numeric columns detected.")
            else:
                selected_num_col = st.selectbox("Select numeric column", num_cols)
                method = st.radio("Outlier detection method", ["IQR", "Z-Score"])

                # 6.3 guard: handle constant columns
                col_data = df_clean[selected_num_col].dropna()

                if method == "IQR":
                    Q1 = col_data.quantile(0.25)
                    Q3 = col_data.quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                else:  # Z-Score — no scipy needed
                    threshold = st.slider("Z-score threshold", 1.0, 5.0, 3.0, 0.1)
                    mean = col_data.mean()
                    std = col_data.std()
                    if std == 0:
                        st.error("Standard deviation is 0 — cannot apply Z-score to a constant column.")
                        st.stop()
                    lower = mean - threshold * std
                    upper = mean + threshold * std

                outlier_mask = (df_clean[selected_num_col] < lower) | (df_clean[selected_num_col] > upper)
                outlier_count = int(outlier_mask.sum())

                st.write(f"**Detected outliers:** {outlier_count} rows | "
                         f"Lower bound: `{lower:.2f}` | Upper bound: `{upper:.2f}`")

                if outlier_count > 0 and st.checkbox("Show outlier rows"):
                    st.dataframe(df_clean[outlier_mask][[selected_num_col]], use_container_width=True)

                action = st.radio("Action", ["Do nothing", "Remove outlier rows", "Cap / Winsorize at quantiles"])

                if action != "Do nothing" and st.button("Apply", key="apply_numeric_clean"):
                    try:
                        before_rows = df_clean.shape[0]
                        if action == "Remove outlier rows":
                            df_clean = df_clean[~outlier_mask]
                            removed = before_rows - df_clean.shape[0]
                            st.success(f"✅ Removed {removed} outlier rows.")
                        elif action == "Cap / Winsorize at quantiles":
                            df_clean[selected_num_col] = df_clean[selected_num_col].clip(lower=lower, upper=upper)
                            st.success(f"✅ Capped {outlier_count} values to [{lower:.2f}, {upper:.2f}].")
                        st.session_state["df"] = df_clean
                        st.session_state["df_clean"] = df_clean
                        log_transformation("Outlier Handling", {"action": action, "method": method}, [selected_num_col])
                        st.dataframe(df_clean[[selected_num_col]].describe(), use_container_width=True)
                    except Exception as e:
                        st.error(f"Error applying outlier action: {e}")

        # ── Scaling / Normalization ─────────────────────
        with cleaning_tabs[5]:
            st.subheader("Scaling / Normalization")
            df_clean = st.session_state["df"].copy()
            numeric_cols = df_clean.select_dtypes(include="number").columns.tolist()

            if not numeric_cols:
                st.info("No numeric columns available for scaling.")
            else:
                # 6.3 guard: validate selection is numeric
                selected_cols = st.multiselect("Select columns to scale", numeric_cols)
                scaling_method = st.radio("Choose scaling method", ["Min-Max Scaling", "Z-score Standardization"])

                if selected_cols:
                    st.write("### Before Scaling Statistics")
                    st.dataframe(df_clean[selected_cols].describe().T[["mean", "std", "min", "max"]], use_container_width=True)

                    if st.button("Apply Scaling"):
                        try:
                            df_scaled = df_clean.copy()
                            if scaling_method == "Min-Max Scaling":
                                for col in selected_cols:
                                    min_val = df_scaled[col].min()
                                    max_val = df_scaled[col].max()
                                    if max_val == min_val:
                                        st.warning(f"Column '{col}' is constant — skipping Min-Max scaling.")
                                        continue
                                    df_scaled[col] = (df_scaled[col] - min_val) / (max_val - min_val)

                            elif scaling_method == "Z-score Standardization":
                                for col in selected_cols:
                                    mean = df_scaled[col].mean()
                                    std = df_scaled[col].std()
                                    if std == 0:
                                        st.warning(f"Column '{col}' has zero std — skipping Z-score.")
                                        continue
                                    df_scaled[col] = (df_scaled[col] - mean) / std

                            st.write("### After Scaling Statistics")
                            st.dataframe(df_scaled[selected_cols].describe().T[["mean", "std", "min", "max"]], use_container_width=True)
                            st.success("Scaling applied successfully ✅")
                            st.subheader("Preview Scaled Data")
                            st.dataframe(df_scaled[selected_cols].head(10), use_container_width=True)
                            st.session_state["df"] = df_scaled
                            log_transformation("Scaling", {"method": scaling_method}, selected_cols)
                        except Exception as e:
                            st.error(f"Scaling failed: {e}")

        # ── Column Operations ───────────────────────────
        with cleaning_tabs[6]:
            st.subheader("Column Operations")
            df_clean = st.session_state["df"].copy()

            st.write("### Rename Column")
            col_to_rename = st.selectbox("Select column", df_clean.columns, key="rename_col")
            new_name = st.text_input("New column name")
            if st.button("Rename Column"):
                if not new_name.strip():
                    st.warning("Enter a new column name.")
                elif new_name in df_clean.columns:
                    st.error(f"Column '{new_name}' already exists.")
                else:
                    try:
                        df_clean = df_clean.rename(columns={col_to_rename: new_name})
                        st.session_state["df"] = df_clean
                        log_transformation("Rename Column", {"from": col_to_rename, "to": new_name}, [col_to_rename])
                        st.success(f"Column '{col_to_rename}' renamed to '{new_name}' ✅")
                    except Exception as e:
                        st.error(f"Error: {e}")

            st.write("### Drop Columns")
            cols_to_drop = st.multiselect("Select columns to drop", df_clean.columns, key="drop_cols")
            if st.button("Drop Selected Columns"):
                if not cols_to_drop:
                    st.warning("Select at least one column.")
                else:
                    try:
                        df_clean = df_clean.drop(columns=cols_to_drop)
                        st.session_state["df"] = df_clean
                        log_transformation("Drop Columns", {}, cols_to_drop)
                        st.success(f"Dropped columns: {cols_to_drop} ✅")
                    except Exception as e:
                        st.error(f"Error: {e}")

            st.write("### Create New Column (Simple Formula)")
            col1_op = st.selectbox("Column A", df_clean.columns, key="formula_col1")
            operation = st.selectbox("Operation", ["+", "-", "*", "/"], key="operation")
            col2_op = st.selectbox("Column B", df_clean.columns, key="formula_col2")
            new_col_name = st.text_input("New column name", key="new_col_name")

            if st.button("Create Column"):
                if not new_col_name.strip():
                    st.warning("Enter a name for the new column.")
                elif not pd.api.types.is_numeric_dtype(df_clean[col1_op]) or not pd.api.types.is_numeric_dtype(df_clean[col2_op]):
                    st.error("Both columns must be numeric for arithmetic operations.")
                else:
                    try:
                        if operation == "+":
                            df_clean[new_col_name] = df_clean[col1_op] + df_clean[col2_op]
                        elif operation == "-":
                            df_clean[new_col_name] = df_clean[col1_op] - df_clean[col2_op]
                        elif operation == "*":
                            df_clean[new_col_name] = df_clean[col1_op] * df_clean[col2_op]
                        elif operation == "/":
                            # 6.3 guard: division by zero
                            if (df_clean[col2_op] == 0).any():
                                st.error("Column B contains zeros — division would produce inf values. Clean that column first.")
                            else:
                                df_clean[new_col_name] = df_clean[col1_op] / df_clean[col2_op]
                        st.session_state["df"] = df_clean
                        log_transformation("Create Column", {"formula": f"{col1_op} {operation} {col2_op}"}, [new_col_name])
                        st.success(f"New column '{new_col_name}' created ✅")
                        st.dataframe(df_clean[[new_col_name]].head(), use_container_width=True)
                    except Exception as e:
                        st.error(f"Error: {e}")

            st.write("### Advanced Column Operations")
            adv_col = st.selectbox("Select column", df_clean.columns, key="adv_col")
            adv_operation = st.selectbox("Choose operation", ["log(col)", "col - mean(col)"], key="adv_op")
            adv_new_col = st.text_input("New column name", key="adv_new_col")

            if st.button("Apply Advanced Operation"):
                if not adv_new_col.strip():
                    st.warning("Enter a name for the new column.")
                elif not pd.api.types.is_numeric_dtype(df_clean[adv_col]):
                    st.error("Selected column must be numeric.")
                else:
                    try:
                        if adv_operation == "log(col)":
                            # 6.3 guard: log of non-positive
                            if (df_clean[adv_col] <= 0).any():
                                st.error("Column contains zero or negative values — log is undefined. Remove or cap them first.")
                            else:
                                df_clean[adv_new_col] = np.log(df_clean[adv_col])
                                st.session_state["df"] = df_clean
                                log_transformation("Advanced Op: log", {}, [adv_col])
                                st.success("Advanced column created ✅")
                                st.dataframe(df_clean[[adv_new_col]].head(), use_container_width=True)
                        elif adv_operation == "col - mean(col)":
                            df_clean[adv_new_col] = df_clean[adv_col] - df_clean[adv_col].mean()
                            st.session_state["df"] = df_clean
                            log_transformation("Advanced Op: demean", {}, [adv_col])
                            st.success("Advanced column created ✅")
                            st.dataframe(df_clean[[adv_new_col]].head(), use_container_width=True)
                    except Exception as e:
                        st.error(f"Error: {e}")

            st.write("### Binning (Convert Numeric → Categories)")
            num_bin_cols = df_clean.select_dtypes(include="number").columns.tolist()
            if not num_bin_cols:
                st.info("No numeric columns available for binning.")
            else:
                bin_col = st.selectbox("Select numeric column", num_bin_cols, key="bin_col")
                bin_type = st.radio("Binning type", ["Equal Width", "Quantile"], key="bin_type")
                bins = st.slider("Number of bins", 2, 10, 4)
                bin_new_col = st.text_input("New binned column name", key="bin_new_col")

                if st.button("Apply Binning"):
                    if not bin_new_col.strip():
                        st.warning("Enter a name for the binned column.")
                    else:
                        try:
                            if bin_type == "Equal Width":
                                df_clean[bin_new_col] = pd.cut(df_clean[bin_col], bins=bins)
                            else:
                                df_clean[bin_new_col] = pd.qcut(df_clean[bin_col], q=bins, duplicates="drop")
                            st.session_state["df"] = df_clean
                            log_transformation("Binning", {"type": bin_type, "bins": bins}, [bin_col])
                            st.success("Binning applied ✅")
                            st.dataframe(df_clean[[bin_col, bin_new_col]].head(), use_container_width=True)
                        except Exception as e:
                            st.error(f"Binning failed: {e}")

        # ── Data Validation ─────────────────────────────
        with cleaning_tabs[7]:
            st.subheader("Data Validation Rules")
            df_clean = st.session_state["df"].copy()
            violations = pd.DataFrame()

            st.write("### Numeric Range Check")
            num_cols_val = df_clean.select_dtypes(include="number").columns.tolist()
            if num_cols_val:
                col_range = st.selectbox("Select numeric column", num_cols_val, key="range_col")
                min_val = st.number_input("Minimum allowed value", value=0.0)
                max_val = st.number_input("Maximum allowed value", value=100.0)

                if st.button("Check Range Violations"):
                    if min_val >= max_val:
                        st.error("Minimum value must be less than maximum value.")
                    else:
                        mask = (df_clean[col_range] < min_val) | (df_clean[col_range] > max_val)
                        range_violations = df_clean[mask].copy()
                        range_violations["Violation"] = f"{col_range} out of range [{min_val}, {max_val}]"
                        violations = pd.concat([violations, range_violations])
                        st.warning(f"Found {len(range_violations)} violations")
                        st.dataframe(range_violations, use_container_width=True)
            else:
                st.info("No numeric columns available.")

            st.write("### Allowed Categories")
            cat_cols_val = df_clean.select_dtypes(include=["object", "category"]).columns.tolist()
            if cat_cols_val:
                col_cat = st.selectbox("Select categorical column", cat_cols_val, key="cat_col")
                allowed_values = st.text_input("Enter allowed values (comma-separated)")
                if st.button("Check Category Violations"):
                    if not allowed_values.strip():
                        st.warning("Enter allowed values first.")
                    else:
                        try:
                            allowed_list = [v.strip() for v in allowed_values.split(",")]
                            mask = ~df_clean[col_cat].isin(allowed_list)
                            cat_violations = df_clean[mask].copy()
                            cat_violations["Violation"] = f"{col_cat} not in allowed list"
                            violations = pd.concat([violations, cat_violations])
                            st.warning(f"Found {len(cat_violations)} violations")
                            st.dataframe(cat_violations, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error checking categories: {e}")
            else:
                st.info("No categorical columns available.")

            st.write("### Non-null Constraint")
            selected_cols_val = st.multiselect("Select columns that must NOT be null", df_clean.columns, key="nonnull_cols")
            if st.button("Check Null Violations"):
                if not selected_cols_val:
                    st.warning("Select at least one column.")
                else:
                    mask = df_clean[selected_cols_val].isnull().any(axis=1)
                    null_violations = df_clean[mask].copy()
                    null_violations["Violation"] = f"Null values in columns: {selected_cols_val}"
                    violations = pd.concat([violations, null_violations])
                    st.warning(f"Found {len(null_violations)} violations")
                    st.dataframe(null_violations, use_container_width=True)

            st.write("### All Violations Summary")
            if not violations.empty:
                st.dataframe(violations, use_container_width=True)
                csv = violations.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Violations Report",
                    data=csv,
                    file_name="violations_report.csv",
                    mime="text/csv"
                )
            else:
                st.info("No violations detected yet.")


# ══════════════════════════════════════════════
# TAB 2 – VISUALIZATION BUILDER
# ══════════════════════════════════════════════

with tabs[2]:
    st.header("Visualization Builder")

    if "df" not in st.session_state:
        st.warning("Please upload and prepare data first")
    else:
        df = st.session_state["df"].copy()

        st.subheader("Filters")
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        if cat_cols:
            filter_col = st.selectbox("Filter by category", ["None"] + cat_cols)
            if filter_col != "None":
                selected_values = st.multiselect(f"Select values for {filter_col}", df[filter_col].dropna().unique())
                if selected_values:
                    df = df[df[filter_col].isin(selected_values)]

        num_cols = df.select_dtypes(include="number").columns.tolist()
        if num_cols:
            num_filter_col = st.selectbox("Filter numeric column", ["None"] + num_cols)
            if num_filter_col != "None":
                min_val = float(df[num_filter_col].min())
                max_val = float(df[num_filter_col].max())
                if min_val < max_val:
                    selected_range = st.slider("Select range", min_val, max_val, (min_val, max_val))
                    df = df[(df[num_filter_col] >= selected_range[0]) & (df[num_filter_col] <= selected_range[1])]

        st.subheader("Chart Builder")
        chart_type = st.selectbox("Select Chart Type", [
            "Histogram", "Box Plot", "Scatter Plot",
            "Line Chart", "Bar Chart", "Correlation Heatmap"
        ])

        x_col = st.selectbox("X-axis", df.columns)
        y_col = st.selectbox("Y-axis (optional)", ["None"] + list(df.columns))
        color_col = st.selectbox("Group/Color (optional)", ["None"] + list(df.columns))
        agg_func = st.selectbox("Aggregation (optional)", ["None", "sum", "mean", "count", "median"])

        try:
            if chart_type == "Histogram":
                if not pd.api.types.is_numeric_dtype(df[x_col]):
                    st.error("Histogram requires a numeric X column.")
                else:
                    fig, ax = plt.subplots()
                    ax.hist(df[x_col].dropna())
                    ax.set_title("Histogram")
                    st.pyplot(fig)

            elif chart_type == "Box Plot":
                if not pd.api.types.is_numeric_dtype(df[x_col]):
                    st.error("Box Plot requires a numeric X column.")
                else:
                    fig, ax = plt.subplots()
                    ax.boxplot(df[x_col].dropna())
                    ax.set_title("Box Plot")
                    st.pyplot(fig)

            elif chart_type == "Scatter Plot":
                if y_col == "None":
                    st.warning("Select a Y column for Scatter Plot.")
                elif not pd.api.types.is_numeric_dtype(df[x_col]) or not pd.api.types.is_numeric_dtype(df[y_col]):
                    st.error("Scatter Plot requires numeric X and Y columns.")
                else:
                    fig, ax = plt.subplots()
                    ax.scatter(df[x_col], df[y_col])
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                    st.pyplot(fig)

            elif chart_type == "Line Chart":
                if y_col == "None":
                    st.warning("Select a Y column for Line Chart.")
                else:
                    df_sorted = df.sort_values(by=x_col)
                    fig, ax = plt.subplots()
                    ax.plot(df_sorted[x_col], df_sorted[y_col])
                    st.pyplot(fig)

            elif chart_type == "Bar Chart":
                if y_col == "None":
                    st.warning("Select a Y column for Bar Chart.")
                else:
                    top_n = st.slider("Top N categories", 1, 20, 10)
                    if agg_func != "None":
                        grouped = df.groupby(x_col)[y_col].agg(agg_func).sort_values(ascending=False).head(top_n)
                    else:
                        grouped = df[x_col].value_counts().head(top_n)
                    fig, ax = plt.subplots()
                    grouped.plot(kind="bar", ax=ax)
                    st.pyplot(fig)

            elif chart_type == "Correlation Heatmap":
                num_df = df.select_dtypes(include="number")
                if num_df.empty:
                    st.error("No numeric columns available for correlation heatmap.")
                else:
                    corr = num_df.corr()
                    fig, ax = plt.subplots()
                    cax = ax.matshow(corr)
                    fig.colorbar(cax)
                    ax.set_xticks(range(len(corr.columns)))
                    ax.set_yticks(range(len(corr.columns)))
                    ax.set_xticklabels(corr.columns, rotation=90)
                    ax.set_yticklabels(corr.columns)
                    st.pyplot(fig)

        except Exception as e:
            st.error(f"Chart error: {e}")

with tabs[3]:
    st.header("Export & Report")

    if "df" not in st.session_state:
        st.warning("Please upload and prepare data first.")
    else:
        df_export = st.session_state["df"]
        log = st.session_state.get("transformation_log", [])

        # ── 1. Export Cleaned Dataset ──────────────────
        st.subheader("Export Cleaned Dataset")

        col1, col2 = st.columns(2)

        with col1:
            csv_data = df_export.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download CSV",
                data=csv_data,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

        with col2:
            from io import BytesIO
            excel_buffer = BytesIO()
            df_export.to_excel(excel_buffer, index=False, engine="openpyxl")
            excel_buffer.seek(0)
            st.download_button(
                label="⬇️ Download Excel",
                data=excel_buffer,
                file_name="cleaned_dataset.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # ── 2. Transformation Report ───────────────────
        st.subheader("Transformation Report")

        if not log:
            st.info("No transformations recorded yet.")
        else:
            log_df = pd.DataFrame(log)
            st.dataframe(log_df, use_container_width=True)

            # CSV version of the log
            report_csv = log_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Transformation Report (CSV)",
                data=report_csv,
                file_name="transformation_report.csv",
                mime="text/csv"
            )

        # ── 3. JSON Recipe ─────────────────────────────
        st.subheader("Export JSON Recipe")
        st.write("A replayable record of every cleaning step with its parameters.")

        import json
        from datetime import datetime

        recipe = {
            "exported_at": datetime.now().isoformat(),
            "total_steps": len(log),
            "steps": log
        }

        recipe_json = json.dumps(recipe, indent=2)
        st.code(recipe_json, language="json")

        st.download_button(
            label="⬇️ Download JSON Recipe",
            data=recipe_json.encode("utf-8"),
            file_name="pipeline_recipe.json",
            mime="application/json"
        )

        # ── 4. Python Script Snippet (stretch) ─────────
        st.subheader("Export Python Script (Pipeline Replay)")
        st.write("A script stub that replays your cleaning steps.")

        script_lines = [
            "import pandas as pd",
            "import numpy as np",
            "",
            "df = pd.read_csv('your_dataset.csv')  # replace with your file",
            "",
        ]

        op_map = {
            "Drop rows with missing values": "df = df.dropna(subset={affected_columns})",
            "Remove Duplicates":             "df = df.drop_duplicates()",
            "Convert to Numeric":            "df[{affected_columns}] = pd.to_numeric(df[{affected_columns}], errors='coerce')",
            "Convert to Categorical":        "df[{affected_columns}] = df[{affected_columns}].astype('category')",
            "Convert to Datetime":           "df[{affected_columns}] = pd.to_datetime(df[{affected_columns}], errors='coerce')",
            "Scaling":                       "# Scaling applied to {affected_columns} — re-apply manually if needed",
            "Outlier Handling":              "# Outlier handling on {affected_columns} — re-apply manually if needed",
            "Drop Columns":                  "df = df.drop(columns={affected_columns})",
            "One-hot Encoding":              "df = pd.get_dummies(df, columns={affected_columns})",
        }

        for step in log:
            op = step["operation"]
            cols = step["affected_columns"]
            template = op_map.get(op, f"# Step: {op} on {cols}")
            line = template.replace("{affected_columns}", str(cols))
            script_lines.append(line)

        script = "\n".join(script_lines)
        st.code(script, language="python")

        st.download_button(
            label="⬇️ Download Python Script",
            data=script.encode("utf-8"),
            file_name="pipeline_replay.py",
            mime="text/plain"
        )

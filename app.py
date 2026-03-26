import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="DataStudio", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@300;400;500;700&display=swap');

/* ── COLOR PALETTE ─────────────────────────────────────── */
:root {
    --green:      #7ccc63;   /* (124, 204, 99)  primary accent  */
    --orange:     #f39c12;   /* (243, 156, 18)  secondary accent */
    --silver:     #bdc3c7;   /* (189, 195, 199) muted / borders  */
    --danger:     #e74c3c;   /* (231,  76, 60)  alerts only      */
    --navy:       #2c3e50;   /* ( 44,  62, 80)  text / headings  */

    --bg:         #f4f6f7;   /* light page background            */
    --surface:    #ffffff;   /* card / sidebar surface           */
    --sidebar-bg: #2c3e50;   /* sidebar uses navy                */
    --text:       #2c3e50;
    --muted:      #7f8c8d;
    --border:     #dde1e3;
}

/* ── BASE ───────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Roboto Serif', serif !important;
    font-size: 13px;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

h1, h2, h3, h4 {
    font-family: 'Roboto Serif', serif !important;
    color: var(--navy) !important;
}

/* ── SIDEBAR ────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: none;
    min-width: 290px;
}

/* all text inside sidebar → light */
section[data-testid="stSidebar"] * {
    color: #ecf0f1 !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    color: var(--green) !important;
    font-size: 16px !important;
    letter-spacing: 0.5px;
}

/* ── SIDEBAR CARDS ──────────────────────────────────────── */
.sb-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 10px;
}

.sb-title {
    font-family: 'Roboto Serif', serif;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--green) !important;
    margin-bottom: 9px;
}

/* ── STAT ROWS ──────────────────────────────────────────── */
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    font-size: 12px;
}
.stat-row:last-child { border-bottom: none; }
.stat-label { color: var(--silver) !important; }
.stat-value {
    font-weight: 700;
    color: #ffffff !important;
    font-size: 12px;
}

/* ── DTYPE BADGES ───────────────────────────────────────── */
.dtype-badge {
    display: inline-block;
    padding: 1px 8px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
}
.dtype-num  { background: rgba(124,204,99,0.2);  color: var(--green)  !important; }
.dtype-cat  { background: rgba(243,156,18,0.2);  color: var(--orange) !important; }
.dtype-date { background: rgba(189,195,199,0.2); color: var(--silver) !important; }
.dtype-bool { background: rgba(124,204,99,0.15); color: var(--green)  !important; }
.dtype-other{ background: rgba(255,255,255,0.1); color: #ecf0f1       !important; }

/* ── COLUMN ROWS ────────────────────────────────────────── */
.col-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 11px;
}
.col-row:last-child { border-bottom: none; }
.col-name {
    color: #ecf0f1 !important;
    max-width: 130px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* ── RESET BUTTON ───────────────────────────────────────── */
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(231,76,60,0.15)  !important;
    border: 1px solid rgba(231,76,60,0.4) !important;
    color: #f1948a !important;
    border-radius: 8px !important;
    # font-size: 12px !important;
    width: 100%;
    transition: all 0.2s;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(231,76,60,0.3) !important;
}

/* ── MAIN AREA ──────────────────────────────────────────── */
.stApp { background: var(--bg); }

.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    padding: 0 1rem;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Roboto Serif', serif !important;
    color: var(--muted) !important;
}
.stTabs [aria-selected="true"] {
    border-color: var(--green) !important;
}

/* ── METRICS ────────────────────────────────────────────── */
div[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    box-shadow: 0 1px 4px rgba(44,62,80,0.06);
}
div[data-testid="metric-container"] label {
    font-size: 10px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--muted) !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: var(--navy) !important;
}

/* success / info messages */
div[data-testid="stAlert"] {
    font-size: 12px;
    border-radius: 8px;
}

/* dataframe */
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* upload widget */
div[data-testid="stFileUploader"] {
    border-radius: 10px;
    border: 1.5px dashed var(--silver) !important;
    background: var(--surface);
    padding: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── Session init ──────────────────────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = None
if "file_name" not in st.session_state:
    st.session_state.file_name = ""

# ── Helpers ───────────────────────────────────────────────────────────────────
def dtype_label(dtype):
    d = str(dtype)
    if "int" in d or "float" in d:    return "num",  "dtype-num"
    if "datetime" in d:               return "date", "dtype-date"
    if "bool" in d:                   return "bool", "dtype-bool"
    if "object" in d or "cat" in d:   return "cat",  "dtype-cat"
    return "?", "dtype-other"

def load_file(file):
    ext = file.name.split(".")[-1].lower()
    if ext == "csv":  return pd.read_csv(file)
    if ext == "xlsx": return pd.read_excel(file)
    if ext == "json": return pd.read_json(file)
    raise ValueError(f"Unsupported format: {ext}")

def sb_card(title, body_html):
    return f'<div class="sb-card"><div class="sb-title">{title}</div>{body_html}</div>'

def stat_row(label, value):
    return f'<div class="stat-row"><span class="stat-label">{label}</span><span class="stat-value">{value}</span></div>'

# ════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🧪 DataStudio")
    st.markdown("---")

    if st.button("↺  Reset Session"):
        st.session_state.df = None
        st.session_state.file_name = ""
        st.rerun()

    st.markdown("---")

    if st.session_state.df is not None:
        df = st.session_state.df

        # ── Dataset info card ─────────────────────────────────
        rows_html = (
            stat_row("File",       st.session_state.file_name) +
            stat_row("Rows",       f"{df.shape[0]:,}") +
            stat_row("Columns",    f"{df.shape[1]}") +
            stat_row("Duplicates", f"{df.duplicated().sum():,}") +
            stat_row("Missing",    f"{df.isnull().sum().sum():,}")
        )
        st.markdown(sb_card("Dataset Info", rows_html), unsafe_allow_html=True)

        # ── Columns & types card ──────────────────────────────
        cols_html = ""
        for col in df.columns:
            lbl, cls = dtype_label(df[col].dtype)
            cols_html += f'''<div class="col-row">
                <span class="col-name" title="{col}">{col}</span>
                <span class="dtype-badge {cls}">{lbl}</span>
            </div>'''
        st.markdown(sb_card("Columns & Types", cols_html), unsafe_allow_html=True)

        # ── Missing values card ───────────────────────────────
        miss = df.isnull().sum()
        miss = miss[miss > 0].sort_values(ascending=False)
        if not miss.empty:
            miss_html = ""
            for col, count in miss.items():
                pct = count / len(df) * 100
                miss_html += f'''<div class="col-row">
                    <span class="col-name" title="{col}">{col}</span>
                    <span style="color:#bdc3c7;font-size:10px">{count} &nbsp;({pct:.1f}%)</span>
                </div>'''
            st.markdown(sb_card("Missing Values", miss_html), unsafe_allow_html=True)
        else:
            st.markdown(sb_card("Missing Values",
                '<div style="font-size:11px;color:#7ccc63">✓ No missing values</div>'),
                unsafe_allow_html=True)

    else:
        st.markdown('<div style="font-size:12px;color:#7f8c8d">Upload a file to see dataset info here.</div>',
                    unsafe_allow_html=True)


# ── MAIN NAVIGATION ───────────────────────────────────────────────────────────
pageA, pageB, pageC, pageD = st.tabs([
    "Upload & Overview",
    "Cleaning Studio",
    "Visualization",
    "Export & Report"
])

with pageA:
    st.title("Upload & Overview")

    uploaded = st.file_uploader(
        "Upload your dataset — CSV, Excel (.xlsx), or JSON",
        type=["csv", "xlsx", "json"],
    )

    if uploaded:
        try:
            df = load_file(uploaded)
            st.session_state.df = df
            st.session_state.file_name = uploaded.name
            st.rerun()
        except Exception as e:
            st.warning(f"Could not load file: {e}")

    if st.session_state.df is None:
        st.info("Upload a file to get started")
    else:
        df = st.session_state.df

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", f"{df.shape[0]:,}")
        c2.metric("Columns", f"{df.shape[1]}")
        c3.metric("Duplicates", f"{df.duplicated().sum():,}")
        c4.metric("Missing", f"{df.isnull().sum().sum():,}")

        st.dataframe(df.head(20), use_container_width=True)


with pageB:
    st.title(" Cleaning & Preparation Studio")

    if st.session_state.df is None:
        st.warning("Upload data first")
    else:
        df = st.session_state.df

        st.subheader("Handle Missing Values")
        col = st.selectbox("Select column", df.columns)

        action = st.selectbox("Choose action", [
            "Drop rows",
            "Fill with mean",
            "Fill with median",
            "Fill with mode"
        ])

        if st.button("Apply Cleaning"):
            if action == "Drop rows":
                df = df.dropna(subset=[col])
            elif action == "Fill with mean":
                df[col] = df[col].fillna(df[col].mean())
            elif action == "Fill with median":
                df[col] = df[col].fillna(df[col].median())
            elif action == "Fill with mode":
                df[col] = df[col].fillna(df[col].mode()[0])

            st.session_state.df = df
            st.success("Transformation applied")

        st.dataframe(df.head(20))

with pageC:
    st.title("📊 Visualization Builder")

    if st.session_state.df is None:
        st.warning("Upload data first")
    else:
        df = st.session_state.df

        chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Histogram"])

        x_col = st.selectbox("X-axis", df.columns)
        y_col = st.selectbox("Y-axis", df.select_dtypes(include="number").columns)

        if st.button("Generate Chart"):
            if chart_type == "Line":
                st.line_chart(df[[x_col, y_col]].set_index(x_col))
            elif chart_type == "Bar":
                st.bar_chart(df[[x_col, y_col]].set_index(x_col))
            elif chart_type == "Histogram":
                st.bar_chart(df[y_col].value_counts())


with pageD:
    st.title("📦 Export & Report")

    if st.session_state.df is None:
        st.warning("Upload data first")
    else:
        df = st.session_state.df

        st.subheader("Download Cleaned Data")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "cleaned_data.csv", "text/csv")

        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        st.download_button("Download Excel", buffer.getvalue(), "cleaned_data.xlsx")

        st.subheader("Transformation Report (Basic)")

        report = {
            "file": st.session_state.file_name,
            "rows": df.shape[0],
            "columns": df.shape[1]
        }

        st.json(report)
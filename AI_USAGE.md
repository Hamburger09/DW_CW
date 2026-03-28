# AI Usage Declaration

## Did you use AI assistance on this project?

Yes. I used Claude (by Anthropic) throughout this project.

---

## What AI Was Used For

- **Generating datasets** — used AI to create sample datasets for testing the application
- **Writing app.py** — AI helped write the Streamlit application code including the cleaning logic, visualization builder, transformation log, and export features
- **Writing README.md** — AI helped structure and write the project documentation
- **Google Colab setup** — AI helped figure out how to run a Streamlit app inside Google Colab using localtunnel
- **Google Sheets integration** — AI helped with the service account registration and gspread setup steps

---

## What I Verified Manually

- **Ran the full application** — launched the app in Google Colab and confirmed it loads correctly in the browser
- **Tested file uploads** — uploaded CSV, Excel, and JSON files and verified they loaded into the app correctly
- **Tested all cleaning tools** — went through each sub-tab in the Cleaning Studio (missing values, duplicates, data types, categorical tools, numeric cleaning, scaling, column operations, data validation) and confirmed they worked as expected
- **Tested the visualization builder** — created multiple chart types and verified they rendered correctly
- **Tested the export tab** — downloaded the cleaned dataset as CSV and Excel, and downloaded the transformation report and JSON recipe
- **Tested undo functionality** — applied transformations and used the Undo Last Step button to confirm it rolled back correctly
- **Read through the code** — went through app.py to understand how the session state, transformation log, caching, and each tab are structured

---

## My Understanding of the Code

After reading through the code I understand:
- How Streamlit session state is used to persist the dataframe across tabs
- How the transformation log snapshots the dataframe before each change to enable undo
- How `@st.cache_data` is used to avoid reloading files on every interaction
- How each cleaning operation modifies the dataframe and saves it back to session state
- How the export tab generates the CSV, Excel, JSON recipe, and Python replay script
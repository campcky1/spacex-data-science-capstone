# SpaceX Falcon 9 — IBM Applied Data Science Capstone materials

## Status and important limitations

This repository package contains **original IBM starter notebooks** supplied by the learner, and **executed supporting analyses based on a separate 56-launch historical dashboard sample**. These are **not interchangeable**: the IBM API exercise may produce a 90-launch dataset, and the starter notebooks have **no saved outputs**. Do not claim the course notebooks were completed/executed. The machine-learning starter marked code-filled has not been run.

The 56-launch dataset in `data/historical_dash_56.csv` was transcribed in an earlier analysis from a public `spacex_launch_dash.csv` shared at:
https://github.com/Ahmed-Nezar/IBM-Data-Science-Capstone-SpaceX/blob/main/spacex_launch_dash.csv
Data provenance and applicability need to be considered when comparing against the course labs. Analytical conclusions apply **only to this historical sample**. This sample lacks date, orbit, precise launch events and infrastructure coordinates, so **yearly trend** and **verified site-to-infrastructure distances** cannot be generated from it. Some plotted flight-number groups are not yearly trends.

## Contents

- `notebooks/course_starters/`: original IBM lab notebooks (not executed) and one code-filled but unexecuted ML notebook.
- `notebooks/executed/Historical_56_launch_analysis_EXECUTED.ipynb`: supporting notebook with saved outputs for the historical sample.
- `notebooks/executed/SQL_EDA_historical_56_EXECUTED.ipynb`: executable SQL analysis with saved SQLite outputs.
- `data/`: historical sample dataset.
- `src/reproduce_analysis.py`: regeneration of analysis plots, SQLite results and model training (fixed to use relative output paths).
- `src/dashboard_app.py`: Dash application with launch-site selection, payload slider, pie chart and scatter plot; it is **runnable code**, not proof of a previously captured live session.
- `results/`: computed charts, SQL output tables, Folium HTML and model evaluation.
- `presentation/`: previous 10/15 submission, **not a verified final passing presentation**.

## Run on your computer

1. Install Python 3.10 or newer.
2. Open a terminal inside this extracted folder and run `python -m pip install -r requirements.txt`.
3. Run `python src/reproduce_analysis.py` (writes to `results/regenerated/`).
4. Run `python src/dashboard_app.py`, then open `http://127.0.0.1:8050/` in your browser.
5. Open notebooks with `jupyter lab`; notebooks under `notebooks/executed` reference the root data folder using relative paths.
6. Open `results/maps/folium_site_map.html` in a browser to inspect the map.

## How to upload to your own GitHub

1. Sign into GitHub and create a new **public** repository, e.g. `spacex-data-science-capstone`.
2. Select **Add file → Upload files**, then upload the **contents of this extracted folder**, keeping folders organized. GitHub web uploads may require adding files one folder at a time. Alternatively use GitHub Desktop to publish the entire folder.
3. Confirm the repository displays notebooks, source code, README and results. Copy your real repository URL.
4. Add that real URL to the methodology and references slides of the PowerPoint; export the PowerPoint to PDF again and upload **the PDF** to the course.

## What is still required for full IBM rubric compliance

- Execute and save outputs from the **original IBM API, web scraping, wrangling, EDA, Folium and ML notebooks** using the course-compatible datasets.
- Complete and capture the *actual* Plotly Dash application with both all-sites and site-filtered views.
- Obtain the correct mission/outcome-specific SQL source for the course SQL lab and its specified queries.
- Capture genuine Folium maps of launch outcomes and measured coast/road/rail proximities using authoritative geographic data.
- Replace supporting sample results in the deck with relevant original lab outputs and insert your actual GitHub URL.

**Uploading this folder to GitHub alone does not resolve all of these rubric requirements.**

"""IBM SpaceX Capstone Plotly Dash, four completed lab tasks.
Run in normal Python (not JupyterLite): python spacex_dash_app.py
Requires: pip install pandas plotly dash
Dataset: bundled historical 56-launch CSV; not the 90-row API dataset.
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

DATA_FILE = Path(__file__).with_name("spacex_launch_dash.csv")
spacex_df = pd.read_csv(DATA_FILE)
required = {"Launch Site", "class", "Payload Mass (kg)", "Booster Version Category"}
missing = required - set(spacex_df.columns)
if missing:
    raise ValueError(f"Missing dataset columns: {sorted(missing)}")
spacex_df["class"] = spacex_df["class"].astype(int)
min_payload = 0
max_payload = 10000
site_options = [{"label":"All Sites", "value":"ALL"}] + [
    {"label": site, "value":site} for site in sorted(spacex_df["Launch Site"].unique())
]

app = Dash(__name__)
app.title = "SpaceX Launch Records Dashboard"
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center", "color": "#204080"}),
    html.P("Historical IBM dashboard sample (56 launches); landing success class = 1."),
    # Task 1: site selection
    dcc.Dropdown(id="site-dropdown", options=site_options, value="ALL",
                 placeholder="Select a Launch Site here", searchable=True, clearable=False),
    dcc.Graph(id="success-pie-chart"),
    html.P("Payload range (kg)"),
    # Task 3: payload filter
    dcc.RangeSlider(id="payload-slider", min=min_payload, max=max_payload,
                    step=1000, value=[min_payload,max_payload],
                    marks={0:"0",2500:"2,500",5000:"5,000",7500:"7,500",10000:"10,000"}),
    dcc.Graph(id="success-payload-scatter-chart"),
], style={"maxWidth":"1150px", "margin":"auto", "fontFamily":"Arial", "padding":"22px"})

# Task 2: all sites => count of successful launches by site; one site => class breakdown.
@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        counts = (spacex_df[spacex_df["class"] == 1]
                  .groupby("Launch Site").size().reset_index(name="Successful Landings"))
        return px.pie(counts, values="Successful Landings", names="Launch Site",
                      title="Successful Landings by Launch Site — All Sites", hole=0.22)
    filtered = spacex_df[spacex_df["Launch Site"] == entered_site]
    counts = filtered["class"].value_counts().reindex([0,1],fill_value=0)
    values = pd.DataFrame({"Outcome": ["Failure", "Success"], "Count":counts.values})
    return px.pie(values, values="Count", names="Outcome",
                  title=f"Landing Outcomes — {entered_site}",
                  color="Outcome", color_discrete_map={"Success":"#238b45", "Failure":"#d34f4f"})

# Task 4: site & payload slider both filter scatter plot, color indicates booster version.
@app.callback(Output("success-payload-scatter-chart", "figure"),
              Input("site-dropdown", "value"), Input("payload-slider", "value"))
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered = spacex_df[spacex_df["Payload Mass (kg)"].between(low,high)].copy()
    if entered_site != "ALL":
        filtered = filtered[filtered["Launch Site"] == entered_site]
    fig = px.scatter(filtered, x="Payload Mass (kg)", y="class",
                     color="Booster Version Category", hover_data=["Launch Site"],
                     title=f"Payload vs. Landing Outcome ({low:,}–{high:,} kg)")
    fig.update_yaxes(tickvals=[0,1], ticktext=["Failure", "Success"], range=[-0.15,1.15])
    return fig

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)

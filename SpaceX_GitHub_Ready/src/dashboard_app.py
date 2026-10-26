"""Run: pip install pandas plotly dash; python dashboard_app.py"""
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
D=Path(__file__).parent
df=pd.read_csv(D.parent/'data'/'historical_dash_56.csv')
app=Dash(__name__)
app.layout=html.Div([
 html.H1('Falcon 9 | Historical Landing Outcomes'),
 html.P('56 launch historical IBM dashboard sample; recovery outcome, not mission success.'),
 dcc.Dropdown(id='site',options=[{'label':'All launch sites','value':'ALL'}]+[{'label':i,'value':i} for i in sorted(df.LaunchSite.unique())],value='ALL'),
 dcc.RangeSlider(id='payload',min=0,max=10000,step=500,value=[0,10000],marks={i:str(i) for i in range(0,10001,2000)}),
 dcc.Graph(id='pie'),dcc.Graph(id='scatter')],style={'maxWidth':'1050px','margin':'auto','fontFamily':'Arial'})
@app.callback(Output('pie','figure'),Output('scatter','figure'),Input('site','value'),Input('payload','value'))
def redraw(site,mass):
 d=df if site=='ALL' else df[df.LaunchSite==site]
 d=d[d.PayloadMass.between(mass[0],mass[1])].copy()
 d['Recovery']=d.Class.map({0:'Not successful',1:'Successful'})
 return (px.pie(d,names='Recovery',title='Recovery outcomes by selected launch site'),
         px.scatter(d,x='PayloadMass',y='FlightNumber',color='Recovery',hover_data=['LaunchSite','BoosterCategory'],title='Payload and flight number'))
if __name__=='__main__':app.run(debug=False)

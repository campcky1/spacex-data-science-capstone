import os, sqlite3, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split,GridSearchCV,StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,ConfusionMatrixDisplay
from pathlib import Path
import folium
P=Path(__file__).resolve().parent.parent / 'results' / 'regenerated'; P.mkdir(parents=True, exist_ok=True)
# Transcribed from public historic IBM spacex_launch_dash.csv (56 rows). See README.md for dataset provenance.
# flight, class, mass, category; each group corresponds to a historical launch site.
groups={
'CCAFS LC-40':[(1,0,0,'v1.0'),(2,0,0,'v1.0'),(3,0,525,'v1.0'),(4,0,500,'v1.0'),(5,0,677,'v1.0'),(7,0,3170,'v1.1'),(8,0,3325,'v1.1'),(9,0,2296,'v1.1'),(10,0,1316,'v1.1'),(11,0,4535,'v1.1'),(12,0,4428,'v1.1'),(13,0,2216,'v1.1'),(14,0,2395,'v1.1'),(15,0,570,'v1.1'),(16,0,4159,'v1.1'),(17,0,1898,'v1.1'),(18,0,4707,'v1.1'),(19,1,1952,'v1.1'),(20,1,2034,'FT'),(22,0,5271,'FT'),(23,1,3136,'FT'),(24,1,4696,'FT'),(25,1,3100,'FT'),(26,0,3600,'FT'),(27,1,2257,'FT'),(28,1,4600,'FT')],
'VAFB SLC-4E':[(6,0,500,'v1.1'),(21,0,553,'v1.1'),(29,1,9600,'FT'),(37,1,9600,'FT'),(40,1,475,'FT'),(42,1,9600,'B4'),(46,0,9600,'FT'),(49,0,2150,'FT'),(51,0,9600,'B4'),(55,0,6460,'B4')],
'KSC LC-39A':[(30,1,2490,'FT'),(31,0,5600,'FT'),(32,1,5300,'FT'),(33,1,3696.65,'FT'),(34,0,6070,'FT'),(35,1,2708,'FT'),(36,1,3669,'FT'),(38,0,6761,'FT'),(39,1,3310,'B4'),(41,1,4990,'B4'),(43,1,5200,'FT'),(44,1,3500,'B4'),(54,1,3600,'B5')],
'CCAFS SLC-40':[(45,1,2205,'FT'),(47,1,3696.65,'B4'),(48,0,4230,'FT'),(50,0,6092,'B4'),(52,0,2647,'B4'),(53,1,362,'B4'),(56,0,5384,'B4')]}
rows=[(f,site,c,m,cat) for site,grp in groups.items() for f,c,m,cat in grp]
df=pd.DataFrame(rows,columns=['FlightNumber','LaunchSite','Class','PayloadMass','BoosterCategory']).sort_values('FlightNumber')
assert len(df)==56 and df.FlightNumber.nunique()==56
df.to_csv(P/'historical_dash_56.csv',index=False)
co=sqlite3.connect(P/'falcon9_sample.db');df.to_sql('SPACEXTBL',co,if_exists='replace',index=False)
queries={
'01_sites':"SELECT LaunchSite, COUNT(*) AS launches FROM SPACEXTBL GROUP BY LaunchSite ORDER BY launches DESC",
'02_site_success':"SELECT LaunchSite, COUNT(*) AS n, SUM(Class) AS successful, ROUND(100.0*AVG(Class),1) AS success_pct FROM SPACEXTBL GROUP BY LaunchSite ORDER BY success_pct DESC",
'03_payload':"SELECT BoosterCategory, COUNT(*) AS flights, ROUND(AVG(PayloadMass),0) AS avg_payload_kg, ROUND(MAX(PayloadMass),0) AS max_payload_kg FROM SPACEXTBL GROUP BY BoosterCategory ORDER BY flights DESC",
'04_success_counts':"SELECT Class, COUNT(*) AS launches FROM SPACEXTBL GROUP BY Class ORDER BY Class DESC",
'05_top_payload':"SELECT FlightNumber, LaunchSite, PayloadMass, Class FROM SPACEXTBL ORDER BY PayloadMass DESC LIMIT 5",
'06_ccafs':"SELECT FlightNumber, LaunchSite, Class FROM SPACEXTBL WHERE LaunchSite LIKE 'CCA%' ORDER BY FlightNumber LIMIT 5",
'07_booster_rank':"SELECT BoosterCategory, COUNT(*) AS flights, SUM(Class) AS successful, ROUND(100.0*AVG(Class),1) AS success_pct FROM SPACEXTBL GROUP BY BoosterCategory ORDER BY success_pct DESC",
'08_payload_range':"SELECT CASE WHEN PayloadMass < 2000 THEN '<2,000 kg' WHEN PayloadMass < 5000 THEN '2,000–4,999 kg' ELSE '5,000+ kg' END AS payload_band, COUNT(*) AS flights, ROUND(100.0*AVG(Class),1) AS success_pct FROM SPACEXTBL GROUP BY payload_band ORDER BY flights DESC",
'09_max_payload':"SELECT FlightNumber, LaunchSite, BoosterCategory, PayloadMass FROM SPACEXTBL WHERE PayloadMass=(SELECT MAX(PayloadMass) FROM SPACEXTBL)",
'10_ranking':"SELECT LaunchSite, COUNT(*) AS flights, SUM(Class) AS successes FROM SPACEXTBL GROUP BY LaunchSite ORDER BY successes DESC",
}
with open(P/'sql_results.txt','w') as out:
 for name,q in queries.items():
  t=pd.read_sql_query(q,co);t.to_csv(P/(name+'.csv'),index=False);out.write(name+'\n'+q+'\n'+t.to_string(index=False)+'\n\n')
co.close()
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
def export(name):plt.tight_layout();plt.savefig(P/(name+'.png'),dpi=160,bbox_inches='tight');plt.close()
for name,xx,yy in [('flight_by_site','FlightNumber','LaunchSite'),('payload_by_site','PayloadMass','LaunchSite'),('flight_by_booster','FlightNumber','BoosterCategory'),('payload_by_booster','PayloadMass','BoosterCategory')]:
 plt.figure(figsize=(9,4.2));order=sorted(df[yy].unique());from matplotlib.lines import Line2D
 for cls,c in [(0,'#db635f'),(1,'#1b8b7b')]:
  d=df[df.Class==cls];plt.scatter(d[xx],[order.index(v) for v in d[yy]],s=60,alpha=.79,c=c,label='Successful' if cls else 'Unsuccessful',edgecolor='white',linewidth=.5)
 plt.yticks(range(len(order)),order);plt.xlabel(xx);plt.legend(loc='best');plt.grid(axis='x',alpha=.15);export(name)
a=df.groupby('BoosterCategory')['Class'].agg(['size','mean']).sort_values('mean',ascending=False);plt.figure(figsize=(8,4));plt.bar(a.index,a['mean']*100,color='#2165a8');plt.ylabel('Landing success (%)');plt.ylim(0,100)
for i,v in enumerate(a['mean']*100):plt.text(i,v+1,f'{v:.0f}% / n={a.iloc[i]["size"]}',ha='center',fontsize=9)
export('success_by_booster')
a=df.groupby('LaunchSite')['Class'].agg(['size','mean']).sort_values('mean',ascending=False);plt.figure(figsize=(9,4));plt.bar(a.index,a['mean']*100,color='#208a95');plt.xticks(rotation=10);plt.ylabel('Landing success (%)');plt.ylim(0,100)
for i,v in enumerate(a['mean']*100):plt.text(i,v+1,f'{v:.0f}% (n={a.iloc[i]["size"]})',ha='center',fontsize=9)
export('success_by_site')
# Flight number proxy trend, since historical Dash file has no date column.
df['flight_bin']=pd.cut(df.FlightNumber,[0,14,28,42,56],labels=['Flights 1–14','15–28','29–42','43–56'])
a=df.groupby('flight_bin',observed=False)['Class'].mean();plt.figure(figsize=(8,4));plt.plot(a.index,a.values*100,marker='o',lw=2.5,color='#2165a8');plt.ylim(0,105);plt.ylabel('Recovery success rate (%)');plt.grid(axis='y',alpha=.18);export('success_by_flight_period')
plt.figure(figsize=(8,4));plt.scatter(df.PayloadMass,df.Class+jitter if False else df.Class,alpha=.66,c=np.where(df.Class==1,'#168a77','#d8615a'));plt.yticks([0,1],['Not successful','Successful']);plt.xlabel('Payload mass (kg)');export('payload_outcome')
# Genuine model fits using the 56-row sample; not presented as official IBM 90-row performance.
X=pd.get_dummies(df[['FlightNumber','PayloadMass','LaunchSite','BoosterCategory']],dtype=int)
y=df.Class
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
cv=StratifiedKFold(n_splits=3,shuffle=True,random_state=42)
models={
'Logistic regression':(Pipeline([('scale',StandardScaler()),('model',LogisticRegression(max_iter=3000))]),{'model__C':[.1,1,10]}),
'SVM':(Pipeline([('scale',StandardScaler()),('model',SVC())]),{'model__C':[.1,1,10],'model__kernel':['linear','rbf','sigmoid']}),
'Decision tree':(DecisionTreeClassifier(random_state=42),{'max_depth':[2,3,4,6],'min_samples_leaf':[1,3]}),
'KNN':(Pipeline([('scale',StandardScaler()),('model',KNeighborsClassifier())]),{'model__n_neighbors':[3,5,7]})}
results=[];preds={}
for name,(est,params) in models.items():
 gs=GridSearchCV(est,params,cv=cv,scoring='accuracy');gs.fit(Xtr,ytr);pred=gs.predict(Xte);preds[name]=pred
 results.append({'Model':name,'CV_Accuracy':round(gs.best_score_,3),'Test_Accuracy':round(accuracy_score(yte,pred),3),'Parameters':str(gs.best_params_)})
res=pd.DataFrame(results).sort_values(['CV_Accuracy','Test_Accuracy'],ascending=False);res.to_csv(P/'model_evaluation.csv',index=False)
best=res.iloc[0]['Model'];ConfusionMatrixDisplay(confusion_matrix(yte,preds[best]),display_labels=['No recovery','Recovery']).plot(cmap='Blues',values_format='d');plt.title('Best CV model: '+best);export('model_confusion')
plt.figure(figsize=(8,4));plt.barh(res.Model,res.Test_Accuracy*100,color='#286cae');plt.xlim(0,100);plt.xlabel('Held-out test accuracy (%)');plt.gca().invert_yaxis()
for i,r in res.reset_index(drop=True).iterrows():plt.text(r.Test_Accuracy*100+1,i,f'{r.Test_Accuracy*100:.1f}%',va='center')
export('model_accuracy')
# Folium map with actual 56-row sample; outcome clusters and count circles.
loc={'CCAFS LC-40':(28.561857,-80.577366),'CCAFS SLC-40':(28.561857,-80.577366),'KSC LC-39A':(28.608058,-80.603956),'VAFB SLC-4E':(34.632093,-120.610829)}
m=folium.Map(location=[32,-102],zoom_start=4)
for site,g in df.groupby('LaunchSite'):
 lat,lon=loc[site];folium.CircleMarker([lat,lon],radius=7+len(g)*.33,popup=f'{site}: {len(g)} flights / {g.Class.sum()} successful',tooltip=site,color='#147f95',fill=True,fill_opacity=.6).add_to(m)
folium.LayerControl().add_to(m);m.save(str(P/'folium_site_map.html'))
# Static geographic evidence plot, not misrepresented as a browser screenshot.
fig,ax=plt.subplots(figsize=(8,4.3));
for site,g in df.groupby('LaunchSite'):
 lat,lon=loc[site];ax.scatter(lon,lat,s=90+len(g)*16,alpha=.65,label=f'{site}: {len(g)} flights');ax.annotate(site,(lon,lat),xytext=(5,7),textcoords='offset points',fontsize=9)
ax.set_xlim(-130,-72);ax.set_ylim(22,40);ax.set_xlabel('Longitude');ax.set_ylabel('Latitude');ax.grid(alpha=.13);ax.legend(loc='upper right',fontsize=8);export('map_site_coordinates')
print('dataset',len(df),'successes',df.Class.sum(),'best',best,'models',res.to_dict(orient='records'))

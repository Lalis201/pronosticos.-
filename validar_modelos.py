"""Validación de origen móvil: datos del libro 1 taller(6).xlsx, sin reentrenamiento con meses futuros."""
import json, math
from pathlib import Path
import numpy as np
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt
from statsmodels.tsa.arima.model import ARIMA
p=Path(__file__).parent
# La serie se distribuye en data_source.json, extraída del libro adjunto.
D=json.loads((p/'data_source.json').read_text(encoding='utf-8'))
y=np.array(D['sales'],float)
methods=['Último valor','Promedio simple','PM12','SES α=0,9','Holt','Regresión lineal','ARIMA (1,1,1)','Estacional ingenuo']
res={m:[] for m in methods}
for t in range(12,36):
    train=y[:t]; actual=y[t]
    pred={'Último valor':train[-1], 'Promedio simple':train.mean(),'PM12':train[-12:].mean(),'Estacional ingenuo':train[-12]}
    pred['SES α=0,9']=float(SimpleExpSmoothing(train,initialization_method='estimated').fit(smoothing_level=.9,optimized=False).forecast(1)[0])
    pred['Holt']=float(Holt(train,initialization_method='estimated').fit(optimized=True).forecast(1)[0])
    pred['Regresión lineal']=float(np.polyval(np.polyfit(np.arange(1,t+1),train,1),t+1))
    try: pred['ARIMA (1,1,1)']=float(ARIMA(train,order=(1,1,1),enforce_stationarity=False,enforce_invertibility=False).fit().forecast(1)[0])
    except Exception: pred['ARIMA (1,1,1)']=float('nan')
    for m,v in pred.items():res[m].append(v)
metrics=[]
for m in methods:
    a=y[12:36];f=np.array(res[m]);mask=np.isfinite(f);e=a[mask]-f[mask]
    metrics.append({'method':m,'mape':round(float(np.mean(np.abs(e/a[mask]))*100),4),'mad':round(float(np.mean(abs(e))),3),'mse':round(float(np.mean(e**2)),3),'me':round(float(np.mean(e)),3),'count':int(mask.sum()),'note':'Validación de origen móvil, 24 predicciones a un paso'})
print('\n'.join(f"{x['method']}: MAPE {x['mape']:.2f}%" for x in metrics))
# Forecast 6 months using entire 36-month history, no future leakage
forecast={}
forecast['Último valor']=[float(y[-1])]*6
forecast['Promedio simple']=[float(y.mean())]*6
forecast['PM12']=[float(y[-12:].mean())]*6
forecast['SES α=0,9']=list(map(float,SimpleExpSmoothing(y,initialization_method='estimated').fit(smoothing_level=.9,optimized=False).forecast(6)))
forecast['Holt']=list(map(float,Holt(y,initialization_method='estimated').fit(optimized=True).forecast(6)))
forecast['Regresión lineal']=list(map(float,np.polyval(np.polyfit(np.arange(1,37),y,1),np.arange(37,43))))
forecast['ARIMA (1,1,1)']=list(map(float,ARIMA(y,order=(1,1,1),enforce_stationarity=False,enforce_invertibility=False).fit().forecast(6)))
forecast['Estacional ingenuo']=list(map(float,y[-12:-6]))
D['validated_metrics']=metrics;D['validated_forecasts']=forecast;D['validation_method']='Origen móvil expansivo; entrenamiento meses 1..t-1 y predicción de t; evaluación enero 2025-diciembre 2026; 24 predicciones a un paso. Parámetros de Holt y ARIMA estimados en cada origen. SES alpha fijo 0.9.'
D['historical_metrics']=D.pop('metrics')
(p/'data_validated.json').write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf-8')
(p/'data.js').write_text('window.PROJECT_DATA = '+json.dumps(D,ensure_ascii=False)+';\n',encoding='utf-8')

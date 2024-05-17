from ib_insync import *
util.startLoop()

import pandas as pd
from datetime import datetime, timedelta
import numpy as numpy
import numpy as np
import schedule
import os
from statistics import mean
from statistics import stdev 
from math import isnan
from itertools import filterfalse
from IPython.display import display
from random import randint
import time
import matplotlib.pyplot as plt
from IPython.display import clear_output


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=randint(0, 10000))

contract = Future('ES', '20240621', 'CME')
contract1 = Future('NQ', '20240621', 'CME')
ib.qualifyContracts(contract)
ib.qualifyContracts(contract1)
ib.reqMarketDataType(1)

ib.sleep(5)

ticker = ib.reqTickByTickData(contract, "Last", 0, False)
ticker1 = ib.reqTickByTickData(contract1, "Last", 0, False)

ib.sleep(1)

TT = ticker.last
TT1 = ticker1.last
ratio = (TT1/TT) * 0.6666666

#creacion de nuevas columnas con los nombres asi :
df3 = pd.DataFrame(columns=['tiempo','es', 'nq', 'ratio'])
df4 = pd.DataFrame(columns=['average1', 'stdev1', 'zz'])
df5 = pd.DataFrame(columns=['Position1'])
df6 = pd.DataFrame(columns=['positionNQ'])
df20 = pd.DataFrame(columns=['positionES'])
df8 = pd.DataFrame(columns=['precio_Es'])
df9 = pd.DataFrame(columns=['precio_Nq'])
df10 = pd.DataFrame(columns=['diferencia_Es'])
df11 = pd.DataFrame(columns=['diferencia_Nq'])
df13 = pd.DataFrame(columns=['dolar_Es'])
df14 = pd.DataFrame(columns=['dolar_Nq'])
df15 = pd.DataFrame(columns=['dollar_Trade'])
df16 = pd.DataFrame(columns=['total_Trade'])
df17 = pd.DataFrame(columns=['positivo'])
df18 = pd.DataFrame(columns=['negativo'])
df19 = pd.DataFrame(columns=['winrate'])
df21 = pd.DataFrame(columns=['position_es_ib'])
df22 = pd.DataFrame(columns=['vende_compra'])
df23 = pd.DataFrame(columns=['number_v_c'])
df24 = pd.DataFrame(columns=['closeES'])
df25 = pd.DataFrame(columns=['closeNQ'])

df7 = pd.concat([df3, df4, df5, df6, df20, df8, df21, df22, df23,  df9, df10, df11, df13, df14, df15, df16, df17, df18, df19,df24,df25], axis=1)    


#esto es para que se agreguen los valores al dataframe
df3.loc[len(df3)] = [datetime.now(), TT, TT1, ratio]              

fib1 = 0.6666666
bb1 = 0.3
bb2 = -0.3
print(ticker)
print(ticker1)


now = datetime.now()
hour = datetime.now().hour
minute = datetime.now().minute
nowsecond = datetime.now().second



ejecutado = False      #esto es para que no se ejecute el codigo  cada minuto en el segundo 00

#se crea la variable PositionIB : 
positionIB = ib.positions()
posES = next((v.position for v in ib.positions() if v.contract.localSymbol == 'ESM4'), 0)
time.sleep(.5)
#posNQ = next((v.position for v in IB.positions() if v.contract.localSymbol == 'NQM4'), 0)

position_es_ib = posES


#obten la hora actual 
now = datetime.now()

#calcula la hora de mañana a las 8:02 am
tomorrow = now + timedelta(days=1) #esto es para calcular la fecha de un dia despues de la fecha actual 

tomorrow_at_802am = datetime(year = tomorrow.year, month = tomorrow.month, day = tomorrow.day, hour = 8,  minute = 2)


def job():
  global ejecutado
  if not ejecutado:
    ejecutado = False
    global contract
    global contract1
    global ticker
    global ticker1
    global TT
    global TT1
    global ratio
    global average1
    global stdev1
    global zz
    global fib1
    global bb1
    global bb2
    global now
    global hour
    global minute
    global util
    global randint
    global Position
    global tiempo
    global df3
    global df4
    global df5
    global df6
    global df7
    global Position1
    global Position2
    global positionIB
    global posES
    global posNQ
    global positionES
    global positionNQ
    global precio_Es
    global position_es_ib
  

    TT = ticker.last
    TT1 = ticker1.last
    ratio = (TT1/TT) * 0.6666666

    df3.loc[len(df3)] = [datetime.now(), TT, TT1, ratio]

    n = 3                          
    series = df3['ratio']           #esto es para que se tome la columna ratio del dataframe
    last3 = series.tail(n = n)      #esto es para que se tomen los ultimos 3 valores
    average1 = last3.mean()         #esto es para que se calcule el promedio de los ultimos 3 valores

    if len(df3) >= 3:
      average1 = df3["ratio"].rolling(3).mean().iloc[-1]
      stdev1 = df3["ratio"].rolling(3).std(ddof=1).iloc[-1]
      zz = (df3['ratio'].iloc[-1] - average1) / stdev1
      negativo = 1
      positivo = 1

      if zz > bb1:               
        Position1 = -1
      elif zz < bb2:
        Position1 = 1
      else: 
        Position1 = 0

      #se crea el valor de positionNQ :
      if Position1 == 0 :
        PositionNQ = df7['positionNQ'].iloc[-1]
      else:
        PositionNQ = Position1

      #se crea el valor de positionES :
      positionES = PositionNQ * -1

      #se crea el valor de precio_Es :
      if positionES != df7['positionES'].iloc[-1]: 
        precio_Es = TT
      else :
        precio_Es = df7['precio_Es'].iloc[-1]

      #se crea el valor de precio_Nq :
      if PositionNQ != df7['positionNQ'].iloc[-1]:
        precio_Nq = TT1
      else :
        precio_Nq = df7['precio_Nq'].iloc[-1]

      #se crea el valor de diferencia_Es :
      if df7['positionES'].iloc[-1] == 0:
        diferencia_Es = 0

      elif df7['positionES'].iloc[-1] > positionES:
        diferencia_Es = precio_Es - df7['precio_Es'].iloc[-1]

      elif df7['positionES'].iloc[-1] < positionES:
        diferencia_Es = df7['precio_Es'].iloc[-1] - precio_Es

      else :
        diferencia_Es = 0


      #se crea el valor de diferencia_Nq :
      if df7['positionNQ'].iloc[-1] == 0:
        diferencia_Nq = 0
      elif df7['positionNQ'].iloc[-1] > PositionNQ:
        diferencia_Nq = precio_Nq - df7['precio_Nq'].iloc[-1]

      elif df7['positionNQ'].iloc[-1] < PositionNQ:
        diferencia_Nq = df7['precio_Nq'].iloc[-1] - precio_Nq

      else :
        diferencia_Nq = 0


      #se crea el valor de dolar_Es :
      dolar_Es = diferencia_Es * 3 * 50 

      #se crea el valor de dolar_Nq :
      dolar_Nq = diferencia_Nq * 2 * 20 

      #se crea el valor de dollar_Trade :
      dollar_Trade = dolar_Es + dolar_Nq

      #arreglo de los valores total_Trade : 
      if PositionNQ == df7['positionNQ'].iloc[-1] :
        dollar_Trade = 0

      #se crea el valor de total_Trade :
      total_Trade = dollar_Trade + df7['total_Trade'].iloc[-1]

      #se crea el valor de positivo y negativo  :
      if dollar_Trade == 0 :
        positivo = df7['positivo'].iloc[-1] 
        negativo = df7['negativo'].iloc[-1] 
      elif dollar_Trade > 0 :
        positivo = df7['positivo'].iloc[-1] + 1
        negativo = df7['negativo'].iloc[-1]
      else  :
        negativo = df7['negativo'].iloc[-1] + 1
        positivo = df7['positivo'].iloc[-1]

      #se crea el valor de winrate :
      winrate = positivo / (positivo + negativo)

      #####################################################ensayo############################################

      posES = next((v.position for v in ib.positions() if v.contract.localSymbol == 'ESM4'), 0)

      position_es_ib = posES

      if positionES == -1 and df7['positionES'].iloc[-1] == 1:
        number_v_c = - 3 - position_es_ib 
        vende_compra = (f'vende')

      elif positionES == 1 and df7['positionES'].iloc[-1] == -1:
        number_v_c = 3 - position_es_ib
        vende_compra = (f'compra')

      else :
        number_v_c = 0
        vende_compra = np.nan

      df7['vende_compra'] = df7['vende_compra'].astype(str)
      #df7['vende_compra'] = vende_compra

      if TT == df7['es'].iloc[-1]:
        closeES = datetime.now()
      else:
        closeES = 0

      if TT1 == df7['nq'].iloc[-1]:
        closeNQ = datetime.now()
      else:
        closeNQ = 0

    else:
      average1 = np.nan 
      stdev1 = np.nan 
      zz = np.nan 
      Position1 = 0
      PositionNQ = 0
      positionES = 0
      precio_Es = 0
      precio_Nq = 0
      diferencia_Es = 0
      diferencia_Nq = 0
      dolar_Es = 0
      dolar_Nq = 0
      dollar_Trade = 0
      total_Trade = 0
      positivo = 1
      negativo = 1
      winrate = 0
      position_es_ib = 0
      vende_compra = np.nan
      number_v_c = 0
      closeES = 0
      closeNQ = 0

    df7.loc[len(df7)] = [datetime.now(), TT, TT1, ratio, average1, stdev1, zz, Position1, PositionNQ, positionES, precio_Es, position_es_ib, vende_compra , number_v_c,
                         precio_Nq, diferencia_Es, diferencia_Nq, dolar_Es, dolar_Nq, dollar_Trade, total_Trade, positivo, negativo, winrate, closeES, closeNQ ] 

    print(contract)
    print(contract1)

    print(f" HORA ACTUAL = {datetime.now()}")
    print(f"ES = {TT}")
    print(f"NQ = {TT1}")
    print(f"RATIO = {ratio}")
    print(f"AVERAGE = {average1}")
    print(f"STDEV = {stdev1}")                                 
    print(f"ZZ = {zz}")
    print(f"POSITION1 = {Position1}")   


    #print(display(df7.tail(n=10)))
    print(display(df7))

    pd.set_option('display.max_rows', None) #esto es para que se muestren todas las filas
    pd.set_option('display.max_columns', None) #esto es para que se muestren todas las columnas
    pd.set_option('max_colwidth', None) #muestra todo el contenido de cada celda

    #grafico de winrate y total trade:

    winrate_1000 = df7['winrate'] * 1000

    #total_Trade = 

    x = df7['tiempo']
    y = df7['total_Trade']

    #rinrate_1000

    x2 = df7['tiempo']
    y2 = winrate_1000

    #se crea la grafica de winrate y total trade

    plt.figure(figsize=(30, 10))
    plt.plot(x, y, marker = 'o',  color='black', linestyle='--', label='total trade')
    plt.plot(x2, y2, marker = 'o', color='r', linestyle='-', label='winrate*1000')
    plt.xlabel('TIME')
    plt.ylabel('WINRATE*1000 Y TOTAL TRADE')
    plt.title('Winrate*1000 and  Total Trade')
    plt.legend()
    plt.show()
    
    
 

    clear_output(wait=True) # esto es para que se borre la grafica anterior y se muestre la nueva
  
    df7.to_csv('df7_17_mayo.csv', index=False) #esto es para que se guarde el dataframe en un archivo csv



def segundo1():
  global ejecutado                                                    # se trae la variable que esta fuera de la funcion
  now = datetime.now()                                                 #se trae la hora actual
  if now.second == 00  :                                                #esto es para que se ejecute el codigo cada minuto
      ejecutado = False                                                #esto es para que se ejecute el codigo cada minuto
      job()   
      ib.sleep(40)  

schedule.every(1).seconds.do(segundo1)                                 #esto es para que se ejecute el codigo cada segundo

while True:
  if datetime.now() >= tomorrow_at_802am:
    print('ya son lasm 8:02 am, se termino el backtesting')
    break 
  schedule.run_pending()
  time.sleep(1)



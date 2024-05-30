from ib_insync import *
util.startLoop()

import pandas as pd
from datetime import datetime, timedelta
import numpy as numpy
import numpy as np
import schedule
from statistics import mean
from statistics import stdev 
from math import isnan
from IPython.display import display
from random import randint
import time
import matplotlib.pyplot as plt
from IPython.display import clear_output

#conexion a interactive brokers
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=randint(0, 10000))

#define los contractos de ES y NQ :
contract = Future('ES', '20240621', 'CME')
contract1 = Future('NQ', '20240621', 'CME')
ib.qualifyContracts(contract)
ib.qualifyContracts(contract1)
ib.reqMarketDataType(1)

ib.sleep(5)

#se crea el tick de ES y NQ : informando que quiere los datos de los ultimos segundos
ticker = ib.reqTickByTickData(contract, "Last", 0, False)
ticker1 = ib.reqTickByTickData(contract1, "Last", 0, False)

ib.sleep(1)

#se crea el valor de TT y TT1 :
TT = ticker.last
TT1 = ticker1.last

ratio = (TT1/TT) * 0.6666666

#creacion de nuevas columnas con los nombres asi :
df3 = pd.DataFrame(columns=['tiempo','es', 'nq', 'ratio', 'average', 'stdev', 'zz', 'position1', 'positionNQ', 'positionES',
                            'precio_Es', 'position_es_ib', 'vende_compra', 'number_v_c','precio_Nq', 'diferencia_Es', 'diferencia_Nq',
                            'dolar_Es', 'dolar_Nq', 'dollar_Trade', 'total_Trade','positivo', 'negativo', 'winrate', 'closeES', 'closeNQ']) 
  
#se imprime los valores de contract y contract1 :
print(ticker)
print(ticker1)

#se crea fib1, bb1 y bb2 para hacer el valor de position1:
fib1 = 0.6666666
bb1 = 0.66666
bb2 = -0.66666

#se define la hora y fecha actual :
now = datetime.now()
hour = datetime.now().hour
minute = datetime.now().minute
nowsecond = datetime.now().second
tomorrow = datetime.now() + timedelta(days=1) #esto es para calcular la fecha de un dia despues de la fecha actual

#se crea la variable PositionIB : 
positionIB = ib.positions()

#calcula la hora de mañana a las 8:02 am
tomorrow_at_802am = datetime(year = tomorrow.year, month = tomorrow.month, day = tomorrow.day, hour = 8,  minute = 2)

#esto es para que no se ejecute el codigo  cada minuto en el segundo 00   
def job():
  global ejecutado
  if not ejecutado:
    ejecutado = False
    global contract
    global contract1
    global ticker
    global ticker1
    global average1
    global stdev1
    global fib1
    global bb1
    global bb2
    global tiempo
    global df3

    #se crea los valores de TT, TT1 y ratio :
    TT = ticker.last
    TT1 = ticker1.last
    ratio = (TT1/TT) * 0.6666666

    #se crea el valor de average1 y stdev1 :
    n = 3                          
    series = df3['ratio']           
    last3 = series.tail(n = n)      
    average1 = last3.mean()         

    if len(df3) >= 3:
      average1 = df3["ratio"].rolling(3).mean().iloc[-1]
      stdev1 = df3["ratio"].rolling(3).std(ddof=1).iloc[-1]
      zz = (df3['ratio'].iloc[-1] - average1) / stdev1
      negativo = 1
      positivo = 1
      positionNQ = 0

      if zz > bb1:               
        Position1 = -1
      elif zz < bb2:
        Position1 = 1
      else: 
        Position1 = 0.0

      #se crea el valor de positionNQ :
      if Position1 == 0 :
        positionNQ = df3['positionNQ'].iloc[-1]
      else:
        positionNQ = Position1

      #se crea el valor de positionES :
      positionES = positionNQ * -1

      #se crea el valor de precio_Es :
      posES = next((v.position for v in ib.positions() if v.contract.localSymbol == 'ESM4'), 0)

      if positionES != df3['positionES'].iloc[-1]: 
        precio_Es = TT
        ib.reqGlobalCancel()
        ib.sleep(0.5)
        
        #se crea el valor de buy_es y sell_es :
        buy_es = abs(3 - (posES))
        sell_es = abs(-3 - (posES))
        
        print(f'posicion IB de ES = {posES}')
       
        print(buy_es)
        print(sell_es)
     
        if positionES != df3['positionES'].iloc[-1] and positionES == 1 and buy_es == 0:
          print('DO NOTHING') 

        elif positionES != df3['positionES'].iloc[-1] and positionES == -1 and sell_es == 0:
          print('DO NOTHING') 

        if  positionES != df3['positionES'].iloc[-1] and buy_es != 0  and positionES == 1 :
          action = LimitOrder( action='BUY',  totalQuantity=  buy_es, lmtPrice= TT)
          ib.placeOrder(contract, action)

        elif  positionES != df3['positionES'].iloc[-1]  and sell_es != 0 and positionES == -1:
          action1 = LimitOrder( action='SELL', totalQuantity= sell_es, lmtPrice= TT)
          ib.placeOrder(contract, action1)

      else:
        precio_Es = df3['precio_Es'].iloc[-1]

      #se crea el valor de nq : 
      posNQ = next((v.position for v in ib.positions() if v.contract.localSymbol == 'NQM4'), 0)

      if positionNQ != df3['positionNQ'].iloc[-1]:
        precio_Nq = TT1
        #ib.sleep(0.5) 

        # se crea el valor de buy_nq y sell_nq :
        buy_nq = abs(2 - (posNQ))
        sell_nq = abs(-2 - (posNQ))

        print(f'posicion IB de NQ = {posNQ}')

        print(buy_nq)
        print(sell_nq)

        if positionNQ != df3['positionNQ'].iloc[-1] and positionNQ == -1 and sell_nq == 0:
            print('DO NOTHING')

        elif positionNQ != df3['positionNQ'].iloc[-1] and positionNQ == 1 and buy_nq == 0:
            print('DO NOTHING')
          
        elif  positionNQ != df3['positionNQ'].iloc[-1]  and buy_nq != 0 and positionNQ == 1:
          action2 = LimitOrder( action='BUY', totalQuantity= buy_nq, lmtPrice= TT1 )
          ib.placeOrder(contract1,  action2)

        if  positionNQ != df3['positionNQ'].iloc[-1]  and sell_nq != 0 and positionNQ == -1:
          action3 = LimitOrder( action='SELL', totalQuantity= sell_nq, lmtPrice= TT1)
          ib.placeOrder(contract1, action3)

      else :
        precio_Nq = df3['precio_Nq'].iloc[-1] 

      #se crea el valor de diferencia_Es :
      if df3['positionES'].iloc[-1] == 0:
        diferencia_Es = 0

      elif df3['positionES'].iloc[-1] > positionES:
        diferencia_Es = precio_Es - df3['precio_Es'].iloc[-1]

      elif df3['positionES'].iloc[-1] < positionES:
        diferencia_Es = df3['precio_Es'].iloc[-1] - precio_Es

      else :
        diferencia_Es = 0

      #se crea el valor de diferencia_Nq :
      if df3['positionNQ'].iloc[-1] == 0:
        diferencia_Nq = 0

      elif df3['positionNQ'].iloc[-1] > positionNQ:
        diferencia_Nq = precio_Nq - df3['precio_Nq'].iloc[-1]

      elif df3['positionNQ'].iloc[-1] < positionNQ:
        diferencia_Nq = df3['precio_Nq'].iloc[-1] - precio_Nq

      else :
        diferencia_Nq = 0

      #se crea el valor de dolar_Es :
      dolar_Es = diferencia_Es * 3 * 50 

      #se crea el valor de dolar_Nq :
      dolar_Nq = diferencia_Nq * 2 * 20 

      #se crea el valor de dollar_Trade :
      dollar_Trade = dolar_Es + dolar_Nq

      #arreglo de los valores total_Trade : 
      if positionNQ == df3['positionNQ'].iloc[-1] : dollar_Trade = 0

      #se crea el valor de total_Trade :
      total_Trade = dollar_Trade + df3['total_Trade'].iloc[-1]

      #se crea el valor de positivo y negativo  :
      if dollar_Trade == 0 :
        positivo = df3['positivo'].iloc[-1] 
        negativo = df3['negativo'].iloc[-1] 
      elif dollar_Trade > 0 :
        positivo = df3['positivo'].iloc[-1] + 1
        negativo = df3['negativo'].iloc[-1]
      else  :
        negativo = df3['negativo'].iloc[-1] + 1
        positivo = df3['positivo'].iloc[-1]

      #se crea el valor de winrate :
      winrate = positivo / (positivo + negativo)

      #se crea el valor de position_es_ib y position_nq_ib:
      position_es_ib = posES
      position_nq_ib = posNQ

      #SE CREA EL VALOR DE VENDE_COMPRA Y NUMBER_V_C :
      vende_compra = np.nan

      if positionES == -1 and df3['positionES'].iloc[-1] == 1:
        number_v_c = - 3 - position_es_ib 
        vende_compra = (f'vende')

      elif positionES == 1 and df3['positionES'].iloc[-1] == -1:
        number_v_c = 3 - position_es_ib
        vende_compra = (f'compra')

      if positionNQ == -1 and df3['positionNQ'].iloc[-1] == 1:
        number_v_c = - 3 - position_nq_ib
        vende_compra = (f'vende')

      elif positionNQ == 1 and df3['positionNQ'].iloc[-1] == -1:
        number_v_c = 3 - position_nq_ib
        vende_compra = (f'compra')

      else :
        number_v_c = 0

     #se crea el valor de closeES  :
      if TT == df3['es'].iloc[-1]:
        closeES = datetime.now()
      else:
        closeES = 0

      #se crea el valor de closeES  :
      if TT1 == df3['nq'].iloc[-1]:
        closeNQ = datetime.now()
      else:
        closeNQ = 0

    else:
      average1 = 0
      stdev1 = 0
      zz = 0
      Position1 = 0
      positionNQ = 0
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
      vende_compra = 0
      number_v_c = 0
      closeES = 0
      closeNQ = 0
      total_commission = 0

    df3.loc[len(df3)] = [datetime.now(), TT, TT1, ratio, average1, stdev1, zz, Position1, positionNQ, positionES, precio_Es, position_es_ib, vende_compra , number_v_c,
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

    print(display(df3))

    pd.set_option('display.max_rows', None) #esto es para que se muestren todas las filas
    pd.set_option('display.max_columns', None) #esto es para que se muestren todas las columnas
    pd.set_option('max_colwidth', None) #muestra todo el contenido de cada celda

    #grafico de winrate y total trade:
    winrate_1000 = df3['winrate'] * 1000

    #total_Trade = 
    x = df3['tiempo']
    y = df3['total_Trade']

    #rinrate_1000
    x2 = df3['tiempo']
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

    # esto es para que se borre la grafica anterior y se muestre la nueva
    clear_output(wait=True)
  
    #esto es para que se guarde el dataframe en un archivo csv
    df3.to_csv('df3_28_mayo.csv', index=False) 

def segundo1():
  global ejecutado                                                    # se trae la variable que esta fuera de la funcion
  now = datetime.now()                                                 #se trae la hora actual
  if now.second == 00 :                                                #esto es para que se ejecute el codigo cada minuto
      ejecutado = False                                                #esto es para que se ejecute el codigo cada minuto
      job()   
      ib.sleep(20)  

schedule.every(1).seconds.do(segundo1)                                 #esto es para que se ejecute el codigo cada segundo

while True:
  if datetime.now() >= tomorrow_at_802am:
    print('ya son las 8:02 am, se termino el backtesting')
    break 
  schedule.run_pending()
  time.sleep(1)


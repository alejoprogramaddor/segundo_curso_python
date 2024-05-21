from ib_insync import *
from random import randint
import time
import datetime 

util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=randint(0, 10000))

contract = Future('ES', '20240621', 'CME')
contract1 = Future('NQ', '20240621', 'CME')


ib.qualifyContracts(contract)
ib.qualifyContracts(contract1)
ib.reqMarketDataType(1)
ib.sleep(3)

ticker = ib.reqTickByTickData(contract, 'Last', 0, False)
ticker1 = ib.reqTickByTickData(contract1, 'Last', 0, False)

ib.sleep(2)

# i changed last to close

TT = ticker.last
TT1 = ticker1.last

print(TT)
print(TT1)
ib.sleep(3)
ib.reqGlobalCancel()

ib.sleep(1)

posES = next((v.position for v in ib.positions() if v.contract.localSymbol == 'ESM4'), 0)
posNQ = next((v.position for v in ib.positions() if v.contract.localSymbol == 'NQM4'), 0)

#######################################################################################################

ppp = 0    # se llama a la variable de cualquier numero 

x = abs(-3 -(posES))         # SELL
x1 = abs(3 -(posES))        #BUY 

y = abs(3 -(posNQ))          #BUY 
y1 = abs(-3 -(posNQ))         #SELL 

#if posES or posNQ == 0:
#    ib.reqGlobalCancel()
#    print('cancel all orders')
#    ib.sleep(0.5)

xa = 'BUY'
xb = 'SELL'

if ppp == 1:
    x = x1 and  xa # buy
    y = y1 and  xb # sell

elif ppp == -1:
    x = x and  xb # sell
    y = y and  xa # buy

else:
   print('nothing')

#######################################################################################################
# cancel all orders 

if pos != 0:
    print(datetime.datetime.now())

if posNQ != 0:
    print(datetime.datetime.now())


action = LimitOrder(
    action= xa ,
    totalQuantity= x ,   
    lmtPrice = TT 
)
order = ib.placeOrder(contract, order=action)  

action1 = LimitOrder(
    action= xb,
    totalQuantity= y ,
    lmtPrice = TT1 
)
order1 = ib.placeOrder(contract1, order=action1)    


if posES == 0 :
    print('DO NOTHING')

if posNQ == 0 :
    print('DO NOTHING')

if posES != 0 :
    order = ib.placeOrder(contract, order=action)

if posNQ != 0 :
    order1 = ib.placeOrder(contract1, order=action1)

#######################################################################################################

if order == 0 or order1 == 0:
    print('no order')
    ib.reqGlobalCancel()
    ib.sleep(0.5)

#######################################################################################################

#prueba de cancelar todas las ordenes si no se cumple la condicion


#    posES or posNQ != action :
#    ib.reqGlobalCancel()

#    if posES or posNQ == 0 :
#    ib.reqGlobalCancel()
#    print('cancel all orders es and nq')
#    ib.sleep(0.5)

#    if posES or posNQ != 0 and :
#    order = ib.placeOrder(contract, order=action)
#    order1 = ib.placeOrder(contract1, order=action1)


#######################################################################################################

ib.sleep(3)

print(order )
print(order1)

print(posES)

print(posNQ)

ib.sleep(30)

ib.reqGlobalCancel()

ib.disconnect()

#ib.orderStatus()

'''
      posES = next((v.position for v in ib.positions() if v.contract.localSymbol == 'ESM4'), 0)
      posNQ = next((v.position for v in ib.positions() if v.contract.localSymbol == 'NQM4'), 0)


      position_es_ib = posES
      position_nq_ib = posNQ

      if positionES == -1 and df7['positionES'].iloc[-1] == 1:
        number_v_c = - 3 - position_es_ib 
        vende_compra = (f'vende')

      elif positionES == 1 and df7['positionES'].iloc[-1] == -1:
        number_v_c = 3 - position_es_ib
        vende_compra = (f'compra')


      if positionNQ == -1 and df7['positionNQ'].iloc[-1] == 1:
        number_v_c = - 3 - position_nq_ib
        vende_compra = (f'vende')

      elif positionNQ == 1 and df7['positionNQ'].iloc[-1] == -1:
        number_v_c = 3 - position_nq_ib
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

############################################################################################################

# LUGAR DE PRUEBAS :

      ppp = 0    # se llama a la variable de cualquier numero 

      if position_es_ib != 0:
          print(datetime.datetime.now())

      if position_nq_ib != 0:
          print(datetime.datetime.now())

      x = abs(-3 -(posES))         # SELL
      x1 = abs(3 -(posES))        #BUY 

      y = abs(3 -(posNQ))          #BUY 
      y1 = abs(-3 -(posNQ))         #SELL 

      xa = 'BUY'
      xb = 'SELL'

      if ppp == 1:
          x = x1 and  xa # buy
          y = y1 and  xb # sell

      elif ppp == -1:
          x = x and  xb # sell
          y = y and  xa # buy

      else:
        print('nothing')

      action = LimitOrder(
          action= xa ,
          totalQuantity= x ,   
          lmtPrice = TT 
      )
      order = ib.placeOrder(contract, order=action)  

      action1 = LimitOrder(
          action= xb,
          totalQuantity= y ,
          lmtPrice = TT1 
      )
      order1 = ib.placeOrder(contract1, order=action1)    

# se cancelan las ordenes si la posicion es diferente a la posicion anterior ya sea en es y en nq 
      if positionES != df7['positionES'].iloc[-1] :
        ib.reqGlobalCancel()
        ib.timesleep(0.5)

#se imprimen las ordenes en la consola de no hacer nada si la posicion es igual a 0
      if position_es_ib == 0 :
          print('DO NOTHING')

      if position_nq_ib == 0 :
          print('DO NOTHING')

      if position_es_ib != 0 :
        ib.placeOrder(contract, order=action)

      if position_nq_ib != 0 :
        ib.placeOrder(contract1, order=action1) '''

from ib_insync import *
from random import randint

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

ib.sleep(3)

print(order )
print(order1)

print(posES)

print(posNQ)

ib.sleep(30)

ib.reqGlobalCancel()

ib.disconnect()

#ib.orderStatus()

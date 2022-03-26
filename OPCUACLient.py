# -*- coding: utf-8 -*-

from opcua import Client
from opcua import Server
import time

url="opc.tcp://127.0.0.1:4840"
client = Client(url)

client.connect()

print("Client Connected")
while True:
    
    temp=client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL.sTemp")
    temperatura=temp.get_value()
    print(temperatura)
    
    turbina=(-0.03697745*temperatura+25.765447387148996)*1000
    print(turbina)

    llega=client.get_node("ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL.vTurb")
    #llegada=llega.get_value()
    llega.set_value(str(turbina))
    
    time.sleep(1)

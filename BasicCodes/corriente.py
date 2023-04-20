import time
import machine
from machine import ADC


#N=0
#sumatoria = 0
#inicial=time.time()
#corriente = 0
while True:
#while (time.time() - inicial) < 0.5:
    adc = machine.ADC()             # create an ADC object
   # adc = ADC()
    apin = adc.channel(pin='P18')   # create an analog pin on P18
    val = apin.voltage()
    voltajeSensor = (val*(1.1/4095))
    #print(val)
    print(voltajeSensor)
    #corriente=voltajeSensor*20.0;
    #sumatoria= float(sumatoria + pow(corriente,0.5))
    #N=N+1
    #print("{:.4f}".format(val))
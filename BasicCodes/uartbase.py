from machine import UART
import time

uart = UART(1, 9600) # 1st argument: UART number: Hardware UART #1
uart.init(9600, bits=8, parity=None, stop=1, rx_buffer_size=4096)
# Write
#uart.write("C,0")
# Read
#print(uart.read()) # Read as much as possible using
#command = input("Introduzca un comando")
#uart.write(b'C,0')
writtenstr = uart.write('\rC,1')
print('\nWRITTEN: ' + str(writtenstr))
s = uart.read(5)
print('\nREAD: ' + str(s))


while True:
  #  uart.write(str(b'C,0'))
  #  time.sleep(10)
    if uart.any() > 0:
        ph = (uart.read(uart.any()))
        print(ph.decode('utf-8'))
        time.sleep_ms(1)
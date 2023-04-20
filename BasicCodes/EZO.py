try:
  import usocket as socket
except:
  import socket
  
from machine import Pin, RTC, UART, reset
import time
import sys
import network
import gc
import machine
gc.collect()


def web_page():
    uart=UART(1, baudrate=9600)
    uart.init(9600, bits=8, parity=UART.EVEN, stop=1)
    ph = str(uart.read(10))  
    html = """<html><head> <title>Wipy Pressure</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>Wipy Pressure</h1> 
  <p>Pressure: <strong>""" + ph + """</strong></p></body></html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a new socket object
s.bind(('', 80))  #Bind socket that accepts tupple variable with IP and port
s.listen(5) #MAX numbers of queued connections.

while True:
  conn, addr = s.accept() #methot to accept the connection
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024) #gets the request received on the newly created socket and saves it
  request = str(request) 
  print('Content = %s' % request)
  response = web_page() #create a variable called response that contains the HTML text returned by the web_page() function
  conn.send('HTTP/1.1 200 OK\n') #send the response to the socket client
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()  # close the cre
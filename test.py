import socket
import socks
import requests

socks.set_default_proxy(socks.HTTP, "127.0.0.1", 8080)
temp = socket.socket
socket.socket = socks.socksocket
print(requests.get('http://myip.ipip.net/').text)

socket.socket=temp
print(requests.get('http://myip.ipip.net/').text)

socket.socket = socks.socksocket
print(requests.get('http://myip.ipip.net/').text)
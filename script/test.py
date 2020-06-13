import sys
import uuid
import base64,os
import subprocess,requests,time
from Crypto.Cipher import AES

str1 = 'touch /tmp/555.txt'
a = base64.b64encode(str1.encode()).decode()


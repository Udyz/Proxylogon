# CVE-2021-26855 Brute Force EMail Exchange Server
<h1>Timeline:</h1>
<p>Monday, March 8, 2021: Update Dumping content...(I'm not done, can u guy help me done this code ;-;)</p>
<p>Tuesday, March 9, 2021: Remake to simple check valid mail</p>
<p>Wednesday, March 10, 2021: Maybe im done this script, now im waiting true cve pre-auth rce</p>
<img src="https://i.imgur.com/qqmEKja.png"/>
<pre>Sometime, some server extract domain tld is wrong</pre>
<pre>Download users.txt list from github or u find it with Google Dork: <code>intext:'@domain.ltd'</code></pre>
<h1>Shodan</h1><br>
https://beta.shodan.io/search?query=http.component%3A%22outlook+web+app%22
<br>https://beta.shodan.io/search?query=http.html%3A%22%2Fowa%22
<img src="https://i.imgur.com/yP2L4EA.png"/>
<h1>Fofa</h1>
<br>https://fofa.so/result?q=title%3D%22Outlook+Web+App%22
<br>https://fofa.so/result?q=%22%2Fowa%22&qbase64=Ii9vd2Ei
<br>https://gist.githubusercontent.com/pikpikcu/fb604e01a7555adb1577a2fbc856022d/raw/ef3025f809c6ca87d22f01914b230d35f39c0ac2/fofa%2520dork-CVE-2021-26855.md
<img src="https://i.imgur.com/Y5y1G2k.png"/>
<h1>Zoomeye</h1>
<br>https://www.zoomeye.org/searchResult?q=%2Fowa
<br><img src="https://i.imgur.com/r3ifnDD.png"/>

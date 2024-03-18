<h1>O2TV Server</h1>

O2TV Server slouží jako alternativa k IPTV Web Serveru pro O2TV 2.0. Lze ho používat buď jako doplněk v Kodi i samostatně. Zatím bude ke stažení tady. Po odladění  a pokud o něj bude zájem ho můžu nechat přidat do repozitáře.

<a href="https://www.xbmc-kodi.cz/prispevek-o2tv-server">Vlákno na fóru XBMC-Kodi.cz</a><br><br>

<b><u>Kodi</u></b>

Nainstalujte doplněk a v jeho nastavení vyplňte přihlašovací údaje, deviceid (libovolný alfanumerický řetězec) a IP adresu nebo jméno serveru. Po uložení nastavení restartujte Kodi nebo zakažte a povolte doplněk.

<b><u>Samostatný skript</u></b>

Rozbalte zip, zkopírujte config.txt.sample na config.txt a v něm vyplňte jméno, heslo, deviceid a IP adresu nebo jméno serveru. Server spusťte z adresáře service.o2tv.server spuštěním python3 server.py..

<b><u>URL</u></b>

Playlist je dustupný na http://<adresa nebo jméno serveru>:<port (defaultně 8081)>/playlist, např. http://127.0.0.1:8081/playlist

EPG lze pak stáhnout z http://<adresa nebo jméno serveru>:<port (defaultně 8081)>/epg, např. http://127.0.0.1:8081/epg

Na http://<adresa nebo jméno serveru>:<port (defaultně 8081)>, např. http://127.0.0.1:8081 je možné stiskem tlačítka vynutit načtení kanálů nebo vytvotvoření nové sessiony.

<b><u>Změny</u></b>
v1.0.7 (18.03.2024)
- ošetření lomítka v názvu kanálu 

v1.0.6 (17.03.2024)
- oprava přehrávání u kanálů bez EPG

v1.0.5 (15.03.2024)
- rozšíření "homepage"

v1.0.4 (13.03.2024)
- oprava přehrání z IPTV Simple Clienta
- oprava catchupu

v1.0.3 (11.03.2024)
- přidání generování EPG (URL /epg)
- přejmenování adresáře na script.o2tv.server

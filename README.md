<h1>O2TV Server</h1>

O2TV Server slouží jako alternativa k IPTV Web Serveru pro O2TV 2.0. Lze ho používat buď jako doplněk v Kodi i samostatně.

<a href="https://www.xbmc-kodi.cz/prispevek-o2tv-server">Vlákno na fóru XBMC-Kodi.cz</a><br><br>

<b><u>Kodi</u></b>

Nainstalujte doplněk a v jeho nastavení vyplňte přihlašovací údaje, deviceid (libovolný alfanumerický řetězec) a IP adresu nebo jméno serveru. Po uložení nastavení restartujte Kodi nebo zakažte a povolte doplněk.

<b><u>Samostatný skript</u></b>

Rozbalte zip, zkopírujte config.txt.sample na config.txt a v něm vyplňte jméno, heslo, deviceid a IP adresu nebo jméno serveru. Server spusťte z adresáře service.o2tv.server spuštěním python3 server.py.<br>
Pokud chcete O2TV Server spustit na linuxu se systemd jako službu, jako root/přes sudo:
- zkopírujte z adresáře scripts soubor o2tv_server.service do /etc/systemd/system/
- systemctl daemon-reload
- systemctl enable o2tv_server
- systemctl start o2tv_server


<b><u>TVheadend</u></b>

Podporu pro TVheadend berte zatím jako experimentální. Také je potřeba počítat s tím, že např. u TVheadendu v CoreELECu může splnění požadavků a zprovoznění komplikovanější než na plnohodnotných linuxových operačních systémech!

Pro použití O2TV Serveru v TVheadendu je potřeba mít na nainstalovaný streamlink a ffmpeg (na stroji s TVH). Pro načtení EPG přes External XMLTV grabber pak ještě socat.

V config.txt zkontrolujte nastavení cesta_streamlink a cesta_ffmpeg (viz config.txt.sample), v případě Kodi pak analogické položky v nastavení. Při vytváření sítě v TVheadendu použijte adresu http://<adresa nebo jméno serveru>:<port (defaultně 8081)>/playlist/tvheadend/streamlink, např. http://127.0.0.1:8081/playlist/tvheadend/streamlink.

U EPG je jednou z variant využití External XMLTV grabberu. Nejprve ho je potřeba v TVheadnedu povolit (Program/Channels - EPG Grabber modules). V adresáři scripts je připravený skript k epg.sh, který stáhne EPG z O2TV Server a obsah pošle External XMLTV grabberu. Zkontrolujte v něm cestu xmltv.sock (vytvoří se po povolení grabberu) a URL O2TV Serveru.

<b><u>URL</u></b>

Playlist je dustupný na http://<adresa nebo jméno serveru>:<port (defaultně 8081)>/playlist, např. http://127.0.0.1:8081/playlist

EPG lze pak stáhnout z http://<adresa nebo jméno serveru>:<port (defaultně 8081)>/epg, např. http://127.0.0.1:8081/epg

Na http://<adresa nebo jméno serveru>:<port (defaultně 8081)>, např. http://127.0.0.1:8081 je možné stiskem tlačítka vynutit načtení kanálů nebo vytvotvoření nové sessiony.

<b><u>Změny</u></b>
v1.2.5 (07.10.2024)
- když se v nastavení adresy serveru použije řezězec IP, nastaví se adresa automaticky

v1.2.4 (04.10.2024)
- ošetření nefunkční stránky na některých platformách

v1.2.3 (05.09.2024)
- do nastavení přidaná možnost nastavit pořadové číslo služby, která se má použít (-1 = poslední)

v1.2.2 (21.06.2024)
- odstranění originálního názvu pořadu z EPG

v1.2.1 (21.04.2024)
- přidaná možnost změna identifikace kanálu z jména na ID

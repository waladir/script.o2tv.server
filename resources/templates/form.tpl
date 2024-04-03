<html>
  <head>
      <title>O2TV Server</title>
  </head>
  <script>
    function myFunction(text) {
      navigator.clipboard.writeText(text);
    }   
  </script
  <body>
    <h2>O2TV Server</h2>
      Diskuze a podpora k O2TV Serveru: <a href="https://www.xbmc-kodi.cz/prispevek-o2tv-server">https://www.xbmc-kodi.cz/prispevek-o2tv-server</a>
    <h3><font color="red">{{ message }}</font></h3>
    <form method="post" action="/">
      <input type="hidden" name="action" value="reset_channels">
      <input type="submit" value="Resetovat kanály">
    </form>
    <form method="post" action="/">
      <input type="hidden" name="action" value="reset_session">
      <input type="submit" value="Resetovat session">
    </form>
    <hr>
    <p>
    <table>
    <tr><td><b>Playlist</b></td><td><a href="{{ playlist_url }}">{{ playlist_url }}</a></td><td><button onclick="myFunction('{{ playlist_url }}')"/><img src="/img/clipboard.png" width="15" height="15"></button></td></tr>
    <tr><td><b>Playlist pro TVheadend<br>(se streamlink):</b></td><td><a href="{{ playlist_tvheadend_streamlink_url }}">{{ playlist_tvheadend_streamlink_url }}</a></td><td><button onclick="myFunction('{{ playlist_tvheadend_streamlink_url }}')"/><img src="/img/clipboard.png" width="15" height="15"></button></td></tr>
    <tr><td><b>EPG</b></td><td><a href="{{ epg_url }}">{{ epg_url }}</a></td><td><button onclick="myFunction('{{ epg_url }}')"/><img src="/img/clipboard.png" width="15" height="15"></button></td></tr>
    <table>
    <hr>
    <h3>Kanály</h3>
    <table>
% for item in playlist:
      <tr><td><img height="30px" width="45px" src="{{ item['logo'] }}"></td><td><a href="{{ item['url'] }}">{{ item['name'] }}</a></td><td><button onclick="myFunction('{{ item['url'] }}')"/><img src="/img/clipboard.png" width="15" height="15"></button></td></tr>
% end
    </table>
  </body>
</html>
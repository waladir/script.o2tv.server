<html>
  <head>
      <title>O2TV Server</title>
  </head>
  <body>
    <h2>O2TV Server</h2>
    <h3><font color="red">{{ message }}</font></h3>
    <form method="post" action="/">
      <input type="hidden" name="action" value="reset_channels">
      <input type="submit" value="Resetovat kanály">
    </form>
    <form method="post" action="/">
      <input type="hidden" name="action" value="reset_session">
      <input type="submit" value="Resetovat session">
    </form>
  </body>
</html>
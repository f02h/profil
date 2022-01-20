<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="Bottle web project template">
        <link rel="icon" href="/static/favicon.ico">
        <title>Project</title>
        <link rel="stylesheet" type="text/css" href="/static/bootstrap.min.css">
        <link rel="stylesheet" href="/static/numpad-light.css"/>
        <script type="text/javascript" src="/static/bootstrap.min.js"></script>
        <script src="/static/numpad.js"></script>
        <style>
            tr td:last-child {
                font-weight:bold;
            }
        </style>
    </head>
    <body>
        <div>
            <div style="width:33%;display:inline-block;">
                <a href="/zaga" class="btn btn-primary" style="display:flex;margin:auto;width:200px;padding: 15px;">Žaga</a>
            </div>
            <div style="width:33%;display:inline-block;">
                <a href="/vrtalka" class="btn btn-secondary" style="display:flex;margin:auto;width:200px;padding: 15px;">Vrtalka</a>
            </div>
            <div style="width:33%;display:inline-block;">
                <a href="/settings" class="btn btn-warning" style="display:flex;margin:auto;width:200px;padding: 15px;">Nastavitve</a>
            </div>
        </div>
        <table border="1" class="table" style="font-size: 40px;">
        %for row in rows:
          <tr>
              <td>
                <a href="/confirmItem/{{row[-1]}}" class="btn btn-success" style="display:flex;margin:auto;width:200px;padding: 15px;">✓</a>
              </td>
          <%
            del row[-1]
          %>
          %for col in row:
            <td>{{col}}</td>
          %end
          </tr>
        %end
        </table>
        <!--<input type="text" id="demoA"/>--!>
    </body>

    <!-- (C) ATTACH NUMPAD -->
    <script>
    window.addEventListener("load", function(){
      // BASIC
      numpad.attach({target: "demoA"});

      // WITH OPTIONS
      numpad.attach({
        target: "demoB",
        max: 10, // 10 DIGITS
        decimal: false
      });
    });
    </script>

</html>
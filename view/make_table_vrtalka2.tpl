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

            tr td:first-child {
                width: 1%;
                white-space: nowrap;
            }

            td {
                border: 0.5px solid;
                padding: 2px !important;
            }
        </style>
    </head>
    <body>
        <div style="position: fixed;top: 0;width: 100%;padding-bottom: 10px;">
            <div style="width:33%;display:inline-block;">
                <a href="/zaga" class="btn btn-primary" style="display:flex;margin:auto;padding: 9px;font-size: 24px;">Žaga</a>
            </div>
            <div style="width:33%;display:inline-block;">
                <a href="/vrtalka" class="btn" style="display:flex;margin:auto;padding: 9px;font-size: 24px;background-color:white;">Vrtalka</a>
            </div>
            <div style="width:33%;display:inline-block;">
                <a href="/settings" class="btn btn-warning" style="display:flex;margin:auto;padding: 9px;font-size: 24px;">Nastavitve</a>
            </div>
        </div>
        <div style="height:56px"></div>
        <table border="1" class="table" style="font-size: 34px;">
        %for row in rows:
          % if not row[-2]:
            <tr style="background: rgb(0 0 0 / 10%); color: #00000040;">
                <td>
                    <a href="/updateVrtalka/{{row[-1]}}" class="btn btn-warning" style="display:inline-block;margin:auto;width:100px;padding: 15px;">&olarr;</a>
                    <a href="/deleteVrtalka/{{row[-1]}}" class="btn btn-danger" style="display:inline-block;margin:auto;width:100px;padding: 15px;">&#x274C;</a>
                </td>
          %end
          % if row[-2]:
          <tr>
            <td>
                <a href="/confirmVrtalka/{{row[-1]}}" class="btn btn-success" style="display:inline-block;margin:auto;width:100px;padding: 15px;">✓</a>
            </td>
          %end

          <%
            del row[-2]
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
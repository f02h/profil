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

            td:nth-child(4),td:nth-child(5),td:nth-child(6) {
                width:130px;
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
        %for project in rows:
            <table border="1" class="table" style="font-size: 34px;margin-bottom:0px">
            <tr>
                <th colspan="6" style="background-color: #dedede54;">{{project}}
                    % if not projectStats[project]:
                        <a href="/updateZagaProject/{{project}}" class="btn btn-warning" style="display:inline-block;margin:auto;width:100px;padding: 15px;float:right;">&olarr;</a>
                        <a href="/deleteZagaProject/{{project}}" class="btn btn-danger" style="display:inline-block;margin:auto;width:100px;padding: 15px;float:right;">&#x274C;</a>
                     %end
                     % if projectStats[project]:
                        <a href="/confirmZagaProject/{{project}}" class="btn btn-success" style="display:inline-block;margin:auto;width:100px;padding: 15px;float:right;">✓</a>
                     %end
                </th>
            </tr>
            %for row in rows[project]:
              % if not rows[project][row][-2]:
                <tr style="background: rgb(0 0 0 / 10%); color: #00000040;">
                    <td>
                        <a href="/updateZaga/{{rows[project][row][-1]}}" class="btn btn-warning" style="display:inline-block;margin:auto;width:100px;padding: 15px;">&olarr;</a>
                        <a href="/deleteZaga/{{rows[project][row][-1]}}" class="btn btn-danger" style="display:inline-block;margin:auto;width:100px;padding: 15px;">&#x274C;</a>
                    </td>
              %end
              % if rows[project][row][-2]:
              <tr>
                <td>
                    <a href="/confirmZaga/{{rows[project][row][-1]}}" class="btn btn-success" style="display:inline-block;margin:auto;width:100px;padding: 15px;">✓</a>
                </td>
              %end

              <%
                del rows[project][row][-2]
                del rows[project][row][-1]
              %>
              %for col in rows[project][row]:
                % if ((isinstance(col, str)) and ("#" in col)):
                    <td style="color:red;">{{col}}</td>
                % end
                % if (((isinstance(col, str)) and ("#" not in col)) or type(col) != str):
                    <td>{{col}}</td>
                % end
              %end
              </tr>
            %end
            </table>
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
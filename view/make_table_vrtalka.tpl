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
            <div style="width:49%;display:inline-block;">
                <a href="/vrtalka" class="btn" style="display:flex;margin:auto;padding: 9px;font-size: 24px;background-color:white;">Vrtalka</a>
            </div>
            <div style="width:50%;display:inline-block;">
                <a href="/settings" class="btn btn-warning" style="display:flex;margin:auto;padding: 9px;font-size: 24px;">Nastavitve</a>
            </div>
        </div>
        <div style="height:56px"></div>

        <form action="/vrtalka" method="get" style="max-width: 500px;margin: auto;background: white;padding: 10px;font-size: 50px;">
            <input class="btn btn-success" style="font-size: 50px;width:550px" type="submit" name="home" value="Home">
            <input class="btn btn-success" style="font-size: 50px;width:550px" type="submit" name="drill" value="Vrtaj">
        </form>

         <input class="btn btn-success" style="font-size: 50px;width:550px"  name="test" value="{{outputv}}">

    </body>
</html>
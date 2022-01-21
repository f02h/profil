import sqlite3
from bottle import route, run, debug, template, request, static_file, error, TEMPLATE_PATH, static_file, redirect
import os, sys
import csv
import re
import bottle
from collections import defaultdict
import serial
import json
from pprint import pprint

# only needed when you run Bottle on mod_wsgi
from bottle import default_app
#TEMPLATE_PATH.insert(0, './profil/view')
bottle.TEMPLATE_PATH.insert(0, '/home/pi/profil/view')

USB_PORT = "/dev/ttyACM0"
usb = serial.Serial(USB_PORT, 115200, timeout=2)

dirname = os.path.dirname(sys.argv[0])

@route('/static/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='./static/asset/css')

@route('/static/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root='./static/asset/js')

def def_value():
    return "Not Present"

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))

@route('/todo')
def todo_list():

    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("SELECT name,qty,dimensions,status FROM todo WHERE status LIKE '1'")
    result = c.fetchall()


    w, h = 4,len(result);
    output = [[0 for x in range(w)] for y in range(h)]
    idx = 0
    for row in result:

        corner = re.search("[0-9]+\/[0-9]+", str(row[0]))
        useDouble = 0

        try:
            if corner.group(0):
                corner = corner.group(0).split("/")
                if corner[0] != corner[1]:
                    useDouble = 1
                else:
                    useDouble = 0
            else:
                useDouble = 0
        except:
            useDouble = 0

        c.execute("SELECT value FROM vars WHERE name LIKE ?", ("dolzinaRoke",))
        result = c.fetchone()
        dolzinaRoke = float(result[0])

        c.execute("SELECT value FROM vars WHERE name LIKE ?", ("debelinaZage",))
        result = c.fetchone()
        debelinaZage = float(result[0])

        calcDimensions = float(round(row[2], 2))
        if useDouble:
            calcDimensions = (calcDimensions * 2) + dolzinaRoke + debelinaZage
        else:
            calcDimensions = calcDimensions + dolzinaRoke + debelinaZage


        output[idx] = [row[0],row[1],row[2], calcDimensions]
        idx += 1

    c.close()
    output = template('make_table', rows=output)
    return output

@route('/zaga')
def todo_list():

    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(DISTINCT project) FROM zaga WHERE izbrisano IS NULL")
    nbrProjects = c.fetchone()[0]

    c.execute("SELECT name,qty,dimensions,project,status,id FROM zaga WHERE izbrisano IS NULL ORDER BY project,status DESC, substr(name, 0, 6) ASC, dimensions DESC")
    result = c.fetchall()


    w, h = 5,len(result);
    output = [[[0 for x in range(w)] for y in range(h)] for z in range(nbrProjects)]
    dict = nested_dict(2, list)
    projectStats = defaultdict(def_value)
    idx = 0
    for row in result:

        projectStats[row[3]] = 0
        corner = re.search("[0-9]+\/[0-9]+", str(row[0]))
        useDouble = 0

        try:
            if corner.group(0):
                corner = corner.group(0).split("/")
                if corner[0] != corner[1]:
                    useDouble = 1
                else:
                    useDouble = 0
            else:
                useDouble = 0
        except:
            useDouble = 0

        c.execute("SELECT value FROM vars WHERE name LIKE ?", ("dolzinaRoke",))
        result = c.fetchone()
        dolzinaRoke = float(result[0])

        c.execute("SELECT value FROM vars WHERE name LIKE ?", ("debelinaZage",))
        result = c.fetchone()
        debelinaZage = float(result[0])

        calcDimensions = float(round(row[2], 2))

        recalcDim = ''


        firstCalc = ''
        secCalc = ''

        if useDouble:
            calcDimensions = (calcDimensions * 2) + debelinaZage
            if calcDimensions < 250:
                recalcDim += ' #'+str(calcDimensions + dolzinaRoke)
                firstCalc = ' #'+str(calcDimensions + dolzinaRoke)
            else:
                recalcDim += ' '+str(calcDimensions)
                firstCalc = ' '+str(calcDimensions)

            if float(round(row[2], 2)) < 250:
                recalcDim += ' (#' + str(float(round(row[2], 2)) + dolzinaRoke)+')'
                secCalc = ' (#' + str(float(round(row[2], 2)) + dolzinaRoke)+')'
            else:
                recalcDim += str(float(round(row[2], 2)))
                secCalc = str(float(round(row[2], 2)))
        else:
            if float(round(row[2], 2)) < 250:
                recalcDim += '#' + str(float(round(row[2], 2)) + dolzinaRoke)
                firstCalc = '#' + str(float(round(row[2], 2)) + dolzinaRoke)
            else:
                recalcDim += str(float(round(row[2], 2)))
                firstCalc = str(float(round(row[2], 2)))

        if row[4]:
            projectStats[row[3]] = 1

        dict[row[3]][idx] = [row[0],int(row[1]),firstCalc, secCalc,row[2], row[4], row[5]]
       # output[row[3]][idx] = [row[0],int(row[1]),row[2], recalcDim, row[4], row[5]]
        idx += 1

    c.close()
    output = template('make_table_zaga', rows=dict, projectStats=projectStats)
    return output

@route('/vrtalka')
def todo_list():

    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(DISTINCT project) FROM vrtalka WHERE izbrisano IS NULL")
    nbrProjects = c.fetchone()[0]

    c.execute(
        "SELECT name,qty,dimensions,project,status,id FROM vrtalka WHERE izbrisano IS NULL ORDER BY project,status DESC, substr(name, 0, 6) ASC, dimensions DESC")
    result = c.fetchall()

    w, h = 5, len(result);
    output = [[[0 for x in range(w)] for y in range(h)] for z in range(nbrProjects)]
    dict = nested_dict(2, list)
    projectStats = defaultdict(def_value)
    idx = 0
    for row in result:

        projectStats[row[3]] = 0

        if row[4]:
            projectStats[row[3]] = 1

        dict[row[3]][idx] = [row[0], int(row[1]), row[2], row[4], row[5]]
        idx += 1

    hearv = ""

    if request.GET.drill:

        c.execute("SELECT value FROM vars WHERE name LIKE 'pozicija'")
        curpozicija = c.fetchone()[0]

        c.execute("SELECT value FROM vars WHERE name LIKE 'hod'")
        curhod = c.fetchone()[0]

        c.execute("SELECT value FROM vars WHERE name LIKE 'povratek'")
        curpovratek = c.fetchone()[0]

        c.execute("SELECT value FROM vars WHERE name LIKE 'povrtavanje'")
        curpovrtavanje = c.fetchone()[0]

        c.execute("SELECT value FROM vars WHERE name LIKE 'povratekpovrtavanje'")
        curpovratekpovrtavanje = c.fetchone()[0]

        ## pozicijaLNull
        ## pozicijaDNull
        ## pozicijaL
        ## pozicijaD
        ## orodjeL
        ## orodjeD
        ## hodL
        ## počasnejePredKoncemHodaL
        ## hitrostPredKoncemHodaL
        ## hodD
        ## počasnejePredKoncemHodaD
        ## hitrostPredKoncemHodaD
        ## povratekL
        ## povratekD
        ## povrtavanjeL
        ## povrtavanjeD


        data = {
            "action": "drill",
            "pozicija": curpozicija*160,
            "hod": curhod,
            "povratek": curpovratek,
            "povrtavanje": curpovrtavanje,
            "povratekpovrtavanje": curpovratekpovrtavanje
        }

        usb.write(json.dumps(data).encode())
        return redirect(request.path)
    elif request.GET.home:

        data = {
            "action": "home",
        }

        usb.write(json.dumps(data).encode())

        hearv = hear()

    elif request.GET.zaga:

        ## hodL
        ## počasnejePredKoncemHoda
        ## hitrostPredKoncemHoda

        data = {
            "action": "cut",
        }

        usb.write(json.dumps(data).encode())

    elif request.GET.pomik:

        data = {
            "action": "move",
        }

        usb.write(json.dumps(data).encode())


    c.close()
    output = template('make_table_vrtalka', rows=dict, projectStats=projectStats, outputv=hearv)
    return output


@route('/vrtalka2')
def todo_list():

    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("SELECT name,qty,dimensions,status,id FROM vrtalka WHERE izbrisano IS NULL ORDER BY status DESC, dimensions ASC")
    result = c.fetchall()


    w, h = 5,len(result);
    output = [[0 for x in range(w)] for y in range(h)]
    idx = 0
    for row in result:
        output[idx] = [row[0],int(row[1]),row[2], row[3], row[4]]
        idx += 1

    c.close()
    output = template('make_table_vrtalka', rows=output)
    return output

@route('/settings', method='GET' )
def todo_list():

    if request.GET.save:
        pozicija = request.GET.pozicija.strip()
        hod = request.GET.hod.strip()
        povratek = request.GET.povratek.strip()
        povrtavanje = request.GET.povrtavanje.strip()
        povratekpovrtavanje = request.GET.povratekPovrtavanje.strip()

        conn = sqlite3.connect('/home/pi/profil/todo.db')
        c = conn.cursor()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'pozicija'", (pozicija,))
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'hod'", (hod,))
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'povratek'", (povratek,))
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'povrtavanje'", (povrtavanje,))
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'povratekpovrtavanje'", (povratekpovrtavanje,))
        conn.commit()

        redirect('/settings')
    else:
        conn = sqlite3.connect('/home/pi/profil/todo.db')
        c = conn.cursor()
        c.execute("SELECT value FROM vars WHERE name LIKE 'pozicija'")
        curpozicija = c.fetchone()[0]

        c.execute("SELECT value FROM vars WHERE name LIKE 'hod'")
        curhod = c.fetchone()[0]

        c.execute("SELECT value FROM vars WHERE name LIKE 'povratek'")
        curpovratek = c.fetchone()[0]

        c.execute("SELECT value FROM vars WHERE name LIKE 'povrtavanje'")
        curpovrtavanje = c.fetchone()[0]

        c.execute("SELECT value FROM vars WHERE name LIKE 'povratekpovrtavanje'")
        curpovratekpovrtavanje = c.fetchone()[0]

        return template('settings', pozicija=float(curpozicija), hod=float(curhod), povratek=float(curpovratek), povrtavanje=float(curpovrtavanje), povratekpovrtavanje=float(curpovratekpovrtavanje))

@route('/new', method='GET')
def new_item():

    if request.GET.save:

        new = request.GET.name.strip()
        dim = request.GET.dimensions.strip()
        conn = sqlite3.connect('/home/pi/profil/todo.db')
        c = conn.cursor()

        c.execute("INSERT INTO todo (name,dimensions,status) VALUES (?,?,?)", (new,dim, 1))
        new_id = c.lastrowid

        conn.commit()
        c.close()

        return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id

    else:
        return template('new_task.tpl')


@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('/home/pi/profil/todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
        conn.commit()

        return '<p>The item number %s was successfully updated</p>' % no
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchone()

        return template('edit_task', old=cur_data, no=no)

@route('/confirmZaga/<no:int>', method='GET')
def edit_item(no):

    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE zaga SET status = 0 WHERE id LIKE ?", (int(no),))
    conn.commit()

    redirect('/zaga')

@route('/updateZaga/<no:int>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE zaga SET status = 1 WHERE id LIKE ?", (int(no),))
    conn.commit()

    redirect('/zaga')

@route('/deleteZaga/<no:int>', method='GET')
def edit_item(no):

    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE zaga SET izbrisano = strftime('%s', 'now') WHERE id LIKE ?", (int(no),))
    conn.commit()

    redirect('/zaga')

@route('/confirmVrtalka/<no:int>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE vrtalka SET status = 0 WHERE id LIKE ?", (int(no),))
    conn.commit()

    redirect('/vrtalka')\

@route('/updateVrtalka/<no:int>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE vrtalka SET status = 1 WHERE id LIKE ?", (int(no),))
    conn.commit()

    redirect('/vrtalka')\

@route('/deleteVrtalka/<no:int>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE vrtalka SET izbrisano = strftime('%s', 'now') WHERE id LIKE ?", (int(no),))
    conn.commit()

    redirect('/vrtalka')

@route('/confirmZagaProject/<no>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE zaga SET status = 0 WHERE project LIKE ?", (str(no),))
    conn.commit()

    redirect('/zaga')

@route('/updateZagaProject/<no>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE zaga SET status = 1 WHERE project LIKE ?", (str(no),))
    conn.commit()

    redirect('/zaga')

@route('/deleteZagaProject/<no>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE zaga SET izbrisano = strftime('%s', 'now') WHERE project LIKE ?", (str(no),))
    conn.commit()

    redirect('/zaga')

@route('/confirmVrtalkaProject/<no>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE vrtalka SET status = 0 WHERE project LIKE ?", (str(no),))
    conn.commit()

    redirect('/vrtalka')

@route('/updateVrtalkaProject/<no>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE vrtalka SET status = 1 WHERE project LIKE ?", (str(no),))
    conn.commit()

    redirect('/vrtalka')

@route('/deleteVrtalkaProject/<no>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("UPDATE vrtalka SET izbrisano = strftime('%s', 'now') WHERE project LIKE ?", (str(no),))
    conn.commit()

    redirect('/vrtalka')

@route('/upload', method=['GET', 'POST'])
def do_upload():
    data = request.files.upload
    if data and data.file:

        category = 'test'
        upload = request.files.get('upload')
        iQty = 1
        if request.GET.quantity:
            iQty = request.GET.quantity
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.csv'):
            return "File extension not allowed."

        save_path = "/tmp/{category}".format(category=category)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path,overwrite=True)

        conn = sqlite3.connect('/home/pi/profil/todo.db')
        c = conn.cursor()

        with open(file_path, newline='', encoding='cp1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    part = row[0].encode().decode("utf-8")
                    qty = re.search("[0-9]+x", str(part))
                    try:
                        if qty.group(0):
                            part = part.lstrip(qty.group(0))
                            qty = qty.group(0).rstrip("x")
                        else:
                            qty = 0
                    except:
                        qty = 0

                    if qty:
                        if "profil" not in str(part):
                            c.execute("INSERT INTO vrtalka (name,qty,dimensions,status,project) VALUES (?,?,?,?,?)",
                                      (part, qty * iQty, float(round(float(row[2]), 2)), 1, name))

                        c.execute("INSERT INTO zaga (name,qty,dimensions,status,project) VALUES (?,?,?,?,?)", (part,qty * iQty,float(round(float(row[2]), 2)), 1, name))
                        conn.commit()
                    line_count += 1
        c.close()

        return "File successfully saved to '{0}'.".format(save_path)

    return template('upload.tpl')


@route('/item<item:re:[0-9]+>')
def show_item(item):

        conn = sqlite3.connect('/home/pi/profil/todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
        result = c.fetchall()
        c.close()

        if not result:
            return 'This item number does not exist!'
        else:
            return 'Task: %s' % result[0]


@route('/help')
def help():

    static_file('help.html', root='.')


@route('/json<json:re:[0-9]+>')
def show_json(json):

    conn = sqlite3.connect('/home/pi/profil/todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}

def hear():
    msg = usb.read_until() # read until a new line
    mystring = msg.decode('ascii')  # decode n return
    return mystring


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


debug(True)
run(host='0.0.0.0',reloader=True)
# remember to remove reloader=True and debug(True) when you move your
# application from development to a productive environment


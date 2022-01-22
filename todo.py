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

USB_PORT = "/dev/ttyACM1"
usb = serial.Serial(USB_PORT, 115200)

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
    dict2 = nested_dict(2, list)
    projectStats = defaultdict(def_value)
    idx = 0
    for row in result:

        projectStats[row[3]] = 0

        if row[4]:
            projectStats[row[3]] = 1

        dict2[row[3]][idx] = [row[0], int(row[1]), row[2], row[4], row[5]]
        idx += 1

    hearv = ""
    dbvars = ""

    if request.GET.drill:

        res = c.execute("SELECT name,value FROM vars").fetchall()
        dictionary = {}
        #dbvars = (Convert(res, dictionary))
        dbvars = dict(res)

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
            "A": "drill",
            "PLN":dbvars["pozicijaLNull"]*160,
            "PDN":dbvars["pozicijaDNull"]*160,
            "PL":dbvars["pozicijaL"]*160,
            "PD":dbvars["pozicijaD"]*160,
            "OL":dbvars["orodjeL"],
            "OD":dbvars["orodjeD"],
            "HL":dbvars["hodL"]*160,
            "PHL":dbvars["pocasnejePredKoncemHodaL"],
            "PHLH":dbvars["hitrostPredKoncemHodaL"],
            "HD":dbvars["hodD"]*160,
            "PHD":dbvars["pocasnejePredKoncemHodaD"],
            "PHDH":dbvars["hitrostPredKoncemHodaD"],
            "POL":dbvars["povratekL"]*160,
            "POD":dbvars["povratekD"]*160,
            "POVL":dbvars["povrtavanjeL"]*160,
            "POVD":dbvars["povrtavanjeD"]*160,
        }

        usb.write(json.dumps(data).encode())
        hearv = hear()
        ##return redirect(request.path)
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
    output = template('make_table_vrtalka', rows=dict2, projectStats=projectStats, outputv=hearv)
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
        pozicijaLNullV = request.GET.pozicijaLNull.strip()
        pozicijaDNullV = request.GET.pozicijaDNull.strip()
        pozicijaLV = request.GET.pozicijaL.strip()
        pozicijaDV = request.GET.pozicijaD.strip()
        orodjeLV = request.GET.orodjeL.strip()
        orodjeDV = request.GET.orodjeD.strip()
        hodLV = request.GET.hodL.strip()
        pocasnejePredKoncemHodaLV = request.GET.pocasnejePredKoncemHodaL.strip()
        hitrostPredKoncemHodaLV = request.GET.hitrostPredKoncemHodaL.strip()
        hodDV = request.GET.hodD.strip()
        pocasnejePredKoncemHodaDV = request.GET.pocasnejePredKoncemHodaD.strip()
        hitrostPredKoncemHodaDV = request.GET.hitrostPredKoncemHodaD.strip()
        povratekLV = request.GET.povratekL.strip()
        povratekDV = request.GET.povratekD.strip()
        povrtavanjeLV = request.GET.povrtavanjeL.strip()
        povrtavanjeDV = request.GET.povrtavanjeD.strip()

        conn = sqlite3.connect('/home/pi/profil/todo.db')
        c = conn.cursor()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'pozicijaLNull'", (pozicijaLNullV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'pozicijaDNull'", (pozicijaDNullV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'pozicijaL'", (pozicijaLV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'pozicijaD'", (pozicijaDV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'orodjeL'", (orodjeLV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'orodjeD'", (orodjeDV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'hodL'", (hodLV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'pocasnejePredKoncemHodaL'", (pocasnejePredKoncemHodaLV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'hitrostPredKoncemHodaL'", (hitrostPredKoncemHodaLV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'hodD'", (hodDV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'pocasnejePredKoncemHodaD'", (pocasnejePredKoncemHodaDV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'hitrostPredKoncemHodaD'", (hitrostPredKoncemHodaDV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'povratekL'", (povratekLV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'povratekD'", (povratekDV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'povrtavanjeL'", (povrtavanjeLV,))
        conn.commit()
        c.execute("UPDATE vars SET value = ? WHERE name LIKE 'povrtavanjeD'", (povrtavanjeDV,))
        conn.commit()

        redirect('/settings')
    else:
        conn = sqlite3.connect('/home/pi/profil/todo.db')
        c = conn.cursor()
        res = c.execute("SELECT name,value FROM vars").fetchall()
        dictionary = {}
        dbvars = dict(res)

        return template('settings', dbdata=dbvars)

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

def Convert(tup, di):
    for a, b in tup:
        di.setdefault(a, '.').append(b)
    return di

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


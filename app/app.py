from typing import List, Dict
import mysql.connector
import simplejson as json
from flask import Flask, request, Response, render_template, redirect

app = Flask(__name__)

dbconfig = {
    'user': 'xuvwzq6wygw6t2gv',
    'password': 'znabbsq170mffx5r',
    'host': 'pxukqohrckdfo4ty.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
    'port': '3306',
    'database': 'hprxc6b8d6lbq5gf'
}


def random_people() -> List[Dict]:
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM random_people')
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


@app.route('/')
def index():
    random_people_data = random_people()
    return render_template('index.html', title='Table View', random_ppl=random_people_data)


@app.route('/cardView/<int:id>', methods=['GET'])
def cardView(id):
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM random_people WHERE id=' + str(id))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', title="Individual Person", random_ppl=result)


@app.route('/table')
def table() -> str:
    js = json.dumps(random_people())
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/form')
def form():
    return render_template('newPerson.html', title='New Person')

@app.route('/newPerson', methods=['POST'])
def new_person():
    inputData = (request.form.get('first_name'), request.form.get('last_name'), request.form.get('email'),
                 request.form.get('phone'), request.form.get('street_address'), request.form.get('city'),
                 request.form.get('state'))
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("INSERT INTO random_people (first_name, last_name, email, phone, street_address, city, state) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % inputData)
    connection.commit()
    cursor.close()
    connection.close()
    return redirect("/", code=302)

@app.route('/editForm/<int:id>', methods=['GET'])
def editform(id):
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM random_people WHERE id=' + str(id))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('editPerson.html', title='Edit Person', person=result[0])


@app.route('/edit/<int:id>', methods=['POST'])
def edit_person(id):
    inputData = (request.form.get('first_name'), request.form.get('last_name'), request.form.get('email'),
                 request.form.get('phone'), request.form.get('street_address'), request.form.get('city'),
                 request.form.get('state'), id)
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "UPDATE random_people t SET t.first_name = '%s', t.last_name = '%s', t.email = '%s', t.phone = '%s', t.street_address = '%s', t.city = '%s', t.state = '%s' WHERE t.id = %s" % inputData)
    connection.commit()
    cursor.close()
    connection.close()
    return redirect("/", code=302)


@app.route('/deleteRecord/<int:id>')
def delete_record(id):
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM random_people WHERE id=%s" % id)
    cursor.execute("SET @count = 0")
    cursor.execute("UPDATE random_people SET random_people.id = @count:= @count + 1")
    cursor.execute("ALTER TABLE random_people AUTO_INCREMENT = 1")
    connection.commit()
    cursor.close()
    connection.close()
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

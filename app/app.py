from typing import List, Dict
import mysql.connector
import simplejson as json
from flask import Flask, Response

app = Flask(__name__)


def cities_import() -> List[Dict]:
    config = {
        'user': 'xuvwzq6wygw6t2gv',
        'password': 'znabbsq170mffx5r',
        'host': 'pxukqohrckdfo4ty.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
        'port': '3306',
        'database': 'hprxc6b8d6lbq5gf'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM random_people')
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


@app.route('/table')
def index() -> str:
    js = json.dumps(cities_import())
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')

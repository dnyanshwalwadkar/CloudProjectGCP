import mysql.connector
from flask import jsonify

CLOUD_SQL_USERNAME = "root"
CLOUD_SQL_PASSWORD = "root"
CLOUD_SQL_DATABASE_NAME = "userdata"
CLOUD_SQL_CONNECTION_NAME = "cloudproject-345422:europe-west2:numberplate"
GAE_ENV = "standard"

db_user = CLOUD_SQL_USERNAME
db_password = CLOUD_SQL_PASSWORD
db_name = CLOUD_SQL_DATABASE_NAME
db_connection_name = "cloudproject-345422:europe-west2:numberplate"

# db_user = os.environ.get('CLOUD_SQL_USERNAME')
# db_password = os.environ.get('CLOUD_SQL_PASSWORD')
# db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
# db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    print(db_connection_name)
    print(db_name)
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    print(unix_socket)
    try:
            # conn = pymysql.connect(user=db_user, password=db_password,
            #                     unix_socket=unix_socket, db=db_name,
            #                     cursorclass=pymysql.cursors.DictCursor
            #                     )
            conn = mysql.connector.connect(user='root', password='root', host='34.105.178.141',
                                    database='userdata')

    except mysql.MySQLError as e:
        print(e)

    return conn


def get_users():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("select * from userdata.user;")

        users = cursor.fetchall()
        print(result,users)

        if len(users) > 0:
            got_user = jsonify(users)
        else:
            got_user = 'No USER in DB'
    conn.close()
    return got_user

def add_users(user):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO user (name, email, phoneno) VALUES(%s, %s, %s)', (user["name"], user["email"], user["phone"]))
    conn.commit()
    conn.close()


def deleteUser(user):
    conn = open_connection()
    with conn.cursor() as cursor:
        print("Entered")
        cursor.execute('DELETE FROM user WHERE email=%s',
                       [user["email"]])
    conn.commit()
    conn.close()

def updateUser(user):
    conn = open_connection()
    with conn.cursor() as cursor:
        print("Entered")
        cursor.execute('UPDATE user SET phoneno = %s WHERE email= %s',[user['phone'],user['email']])
    conn.commit()
    conn.close()

def addPlate(plate):
    conn = open_connection()
    with conn.cursor() as cursor:
        print("Entered")
        cursor.execute('INSERT INTO plate (plate) VALUES(%s)', [plate])
    conn.commit()
    conn.close()



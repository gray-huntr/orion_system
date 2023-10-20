from myapp import myapp as app
import pymysql


def connect():
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"], database=app.config["DB_NAME"])
    return conn.cursor()


def authenticate(cursor, username, password):
    cursor.execute("select * from clients where username = %s and password = %s", (username, password))
    account = cursor.fetchone()
    if account:
        return True
    else:
        return False


def signup(cursor, fullname, email, password):
    try:
        cursor.execute("insert into clients (fullname, email, password) values (%s , %s, %s)",
                       (fullname, email, password))
        cursor.conection.commit()
        return True
    except pymysql.IntegrityError:
        return False

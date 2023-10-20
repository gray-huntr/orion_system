from myapp import myapp as app
import pymysql


def establish_connection():
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"], database=app.config["DB_NAME"])
    return conn.cursor()


def authenticate(cursor, username, password):
    cursor.execute("select * from clients where username = %s and password = %s", (username, password))
    return cursor.rowcount

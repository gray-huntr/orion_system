from myapp import myapp,server

if __name__ == '__main__':
    myapp.run(debug=True, port=2070)
    server.setup_db()
    
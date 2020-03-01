from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import hashlib
import datetime
import uuid

app=Flask(__name__)

@app.route("/")
def index():
    #SQLite3 DB-Connection
    conn = sqlite3.connect("userstore.db", check_same_thread=False)
    #SQLite3 DB-Cursor
    curs = conn.cursor()

    # Session_Token abfragen
    session_token = str(request.cookies.get("session_token"))

    # CREATE
    curs.execute("""CREATE TABLE IF NOT EXISTS User(
            id integer primary key autoincrement, 
            username text,
            usermail text,
            usernumber text,
            usertext text, 
            timestamp text, 
            session_token text
            );
        """)

    #SQLite3 DB-Cursor schließen
    curs.close()
    #SQLite3 DB-Connection schließen
    conn.close()

    return render_template("index.html")

@app.route("/anfahrt")
def anfahrt():
    return render_template("anfahrt.html")

@app.route("/buchen", methods=["GET", "POST"])
def buchen():
    if request.method == "GET":
        return render_template("buchen.html")

    elif request.method == "POST":

        #SQLite3 DB-Connection
        conn = sqlite3.connect("userstore.db", check_same_thread=False)
        #SQLite3 DB-Cursor
        curs = conn.cursor()

        username = request.form.get("txtName")
        usermail = request.form.get("txtEmail")
        usernumber = request.form.get("txtPhone")
        usertext = request.form.get("txtMsg")

        # Zeitstempel
        created = str(datetime.datetime.now())
        # Session Token
        session_token = str(uuid.uuid4())

        # UPDATE (INSERT)
        curs.execute("""
            INSERT INTO User (username, usermail, usernumber, usertext, timestamp, session_token)
            VALUES (?, ?, ?, ?, ?, ?)
            """, 
            (username, usermail, usernumber, usertext, created, session_token)
        )
        conn.commit()

        print(username)
        print(usermail)
        print(usernumber)
        print(usertext)
        print(created)

        

        #SQLite3 DB-Cursor schließen
        curs.close()
        #SQLite3 DB-Connection schließen
        conn.close()

        

        # Response definieren
        response = redirect(url_for('success'))
        # Cookies setzen
        response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')

        return response

        # Laden der Seite mit dem Parameter user
        #return render_template("success.html", user=user)

@app.route("/success")
def success():

    #SQLite3 DB-Connection
    conn = sqlite3.connect("userstore.db", check_same_thread=False)
    #SQLite3 DB-Cursor
    curs = conn.cursor()

    # Session_Token abfragen
    session_token = str(request.cookies.get("session_token"))

    # READ
    curs.execute(
        """
            SELECT username
            FROM User
            WHERE session_token = ?
        """,
        (session_token,)
    )

    # Auslesen der Daten
    rows = curs.fetchall()
    user=""
    for row in rows:
        user=row

    print(user)

    #SQLite3 DB-Cursor schließen
    curs.close()
    #SQLite3 DB-Connection schließen
    conn.close()

    # Laden der Seite mit dem Parameter user
    return render_template("success.html", user=user)

@app.route("/raeume")
def raeume():
    return render_template("raeume.html")

@app.route("/ueber_uns")
def ueber_uns():
    return render_template("ueber_uns.html")


if __name__ == '__main__':
    app.run(debug=True)
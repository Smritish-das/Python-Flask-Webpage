from flask import Flask,render_template, request, redirect,url_for
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect('test.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Trip( 
desti VARCHAR(20) PRIMARY KEY,
adate DATE,
rdate DATE,
des VARCHAR(50));""")
connection.commit()
connection.close()

@app.route('/')
def hello_world() :
    return render_template('intro.html')

@app.route('/contact')
def contact() :
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Trip")
    ans = cursor.fetchall()
    connection.close()
    return render_template('index.html', trips=ans)

@app.route('/add_trip', methods=['POST'])
def add_trip():
    destination = request.form['des']
    adate = request.form['adate']
    rdate = request.form['rdate']
    note = request.form['de']
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO Trip (desti,adate,rdate,des) VALUES (?, ?, ?, ?)", (destination, adate, rdate,note))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/remove_trip',methods=['POST'])
def delete_input():
    xy = request.form['xyz']

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    delete_statement = "DELETE FROM Trip WHERE desti = ?"

    try:
        cursor.execute(delete_statement, (xy,))
        conn.commit()
        print("Input deleted successfully.")
    except sqlite3.Error as e:
        print("Error deleting input:", e)
    finally:
        conn.close()
        return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug = True)
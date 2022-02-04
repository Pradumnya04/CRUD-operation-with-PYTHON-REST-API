from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("emp_data.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/emp", methods=["GET", "POST"])
def emps():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM emps")
        emps = [
            dict(id=row[0], First_Name=row[1], Last_Name=row[2], Company_Name=row[3], Branch=row[4])
            for row in cursor.fetchall()
        ]
        if emps is not None:
            return jsonify(emps)

    if request.method == "POST":
        First_Name = request.form["First_Name"]
        Last_Name = request.form["Last_Name"]
        Company_Name = request.form["Company_Name"]
        Branch = request.form["Branch"]
        sql = """INSERT INTO emps (First_Name, Last_Name, Company_Name,Branch)
                 VALUES (?, ?, ?, ?)"""
        cursor = cursor.execute(sql, (First_Name, Last_Name, Company_Name, Branch))
        conn.commit()
        return f"employee with the id: 0 created successfully", 201


@app.route("/emp/<int:id>", methods=[ "GET", "PUT", "DELETE"])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM emps WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            emps = r
        if emps is not None:
            return jsonify(emps), 200
        else:
            return "Something wrong", 404
    if request.method == "PUT":
        sql = """UPDATE emps SET First_Name=?, Last_Name=?, Company_Name=?, Branch=? WHERE id=? """
        First_Name = request.form["First_Name"]
        Last_Name = request.form["Last_Name"]
        Company_Name = request.form["Company_Name"]
        Branch = request.form["Branch"]
        updated_emp = {
            "id": id,
            "First_Name": First_Name,
            "Last_Name": Last_Name,
            "Company_Name": Company_Name,
            "Branch": Branch
        }
        conn.execute(sql, (First_Name, Last_Name, Company_Name, Branch, id))
        conn.commit()
        return jsonify(updated_emp)

    if request.method == "DELETE":
        sql = """ DELETE FROM emps WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The emp with id: {} has been deleted.".format(id), 200


if __name__ == "__main__":
    app.run(debug=True)

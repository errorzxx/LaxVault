from flask import Flask, render_template, request, redirect, session
import sqlite3
from utils.encryption import encrypt_data
app = Flask(__name__)
app.secret_key = "laxvault_secret_key"
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    role = request.form.get("role")

    if role == "client":
        return redirect("/client")

    elif role == "lawyer":
        return redirect("/lawyer")

    elif role == "admin":
        return redirect("/admin")

    return redirect("/")



@app.route("/client")
def client_dashboard():

    db = get_db()
    lawyers = db.execute("SELECT * FROM lawyers").fetchall()

    return render_template("client_dashboard.html", lawyers=lawyers)


from utils.encryption import decrypt_data

@app.route("/lawyer")
def lawyer_dashboard():

    db = get_db()
    cases = db.execute("SELECT * FROM cases").fetchall()

    decrypted_cases = []

    for c in cases:
        decrypted_cases.append({
            "id": c["id"],
            "case_details": decrypt_data(c["case_details"])
        })

    return render_template("lawyer_dashboard.html", cases=decrypted_cases)

@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")


@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        print(name,email,password)

        return redirect("/")

    return render_template("signup.html")

@app.route("/hire/<int:lawyer_id>")
def hire_lawyer(lawyer_id):

    return render_template("submit_case.html", lawyer_id=lawyer_id)

@app.route("/submit_case", methods=["POST"])
def submit_case():

    lawyer_id = request.form["lawyer_id"]
    case = request.form["case_details"]

    encrypted_case = encrypt_data(case)

    db = get_db()

    db.execute(
        "INSERT INTO cases (lawyer_id, case_details) VALUES (?,?)",
        (lawyer_id, encrypted_case)
    )

    db.commit()

    return "Case submitted securely!"   

@app.route("/case/<int:case_id>")
def view_case(case_id):

    db = get_db()

    case = db.execute(
        "SELECT * FROM cases WHERE id = ?",
        (case_id,)
    ).fetchone()

    return render_template("case_details.html", case=case)

if __name__ == "__main__":
    app.run(debug=True)

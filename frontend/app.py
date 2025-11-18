from flask import Flask, render_template, request, redirect, session, url_for, abort
import requests
import os

app = Flask(__name__)
app.secret_key = "frontend_secret_key"

BACKEND_URL = "http://nginx/api"   # nginx dentro do compose

# -----------------------------------------
# Helpers
# -----------------------------------------

def auth_headers():
    if "token" in session:
        return {"Authorization": f"Bearer {session['token']}"}
    return {}

# -----------------------------------------
# Rotas
# -----------------------------------------

@app.route("/")
def home():
    return redirect("/raffles")

# ---------------------- LOGIN ----------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = {
            "email": request.form["email"],
            "password": request.form["password"]
        }

        resp = requests.post(f"{BACKEND_URL}/auth/login", json=data)

        if resp.status_code == 200:
            body = resp.json()
            session["token"] = body["token"]
            session["user"] = body["user"]
            return redirect("/raffles")
        else:
            return render_template("login.html", error=resp.json().get("error"))

    return render_template("login.html")

# ---------------------- REGISTER ----------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"]
        }

        resp = requests.post(f"{BACKEND_URL}/auth/register", json=data)
        if resp.status_code == 200:
            return redirect("/login")
        else:
            return render_template("register.html", error=resp.json().get("error"))

    return render_template("register.html")

# ---------------------- LISTA SORTEIOS ----------------------

@app.route("/raffles")
def raffles():
    resp = requests.get(f"{BACKEND_URL}/raffles/")
    raffles = resp.json()

    search_term = request.args.get("q", "").strip()
    only_mine = request.args.get("mine") not in (None, "", "0", "false", "False")

    filtered = raffles

    if search_term:
        lowered = search_term.lower()
        filtered = [
            raffle for raffle in filtered
            if lowered in raffle.get("title", "").lower()
        ]

    if only_mine and session.get("user"):
        user_id = session["user"]["id"]
        filtered = [
            raffle for raffle in filtered
            if raffle.get("creator_id") == user_id
        ]
    elif only_mine:
        only_mine = False  # não há usuário logado, então ignora filtro

    filters = {
        "q": search_term,
        "mine": only_mine
    }

    return render_template("raffles.html", raffles=filtered, filters=filters)

# ---------------------- DETALHE ----------------------

@app.route("/raffles/<int:rid>")
def raffle_detail(rid):
    resp = requests.get(f"{BACKEND_URL}/raffles/{rid}")
    if resp.status_code != 200:
        abort(resp.status_code)
    raffle = resp.json()
    return render_template("raffle_detail.html", raffle=raffle)
# ---------------------- CRIAR ----------------------

@app.route("/raffles/create", methods=["POST"])
def create_raffle():
    data = {
        "title": request.form["title"],
        "description": request.form["description"]
    }
    resp = requests.post(
        f"{BACKEND_URL}/raffles/", 
        json=data, 
        headers=auth_headers()
    )
    return redirect("/raffles")

# ---------------------- ENTRAR ----------------------

@app.route("/raffles/<int:rid>/join", methods=["POST"])
def join_raffle(rid):
    requests.post(
        f"{BACKEND_URL}/raffles/{rid}/join",
        headers=auth_headers()
    )
    return redirect(f"/raffles/{rid}")

# ---------------------- INICIAR ----------------------

@app.route("/raffles/<int:rid>/start", methods=["POST"])
def start_raffle(rid):
    requests.post(
        f"{BACKEND_URL}/raffles/{rid}/start",
        headers=auth_headers()
    )
    return redirect(f"/raffles/{rid}")

# ---------------------- LOGOUT ----------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

from flask import Flask, request, render_template, redirect
import os
import time

app = Flask(__name__)

# ===== Paths =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "files")
FLAG_PATH = os.path.join(BASE_DIR, "flag.txt")
LAST_RESET_FILE = os.path.join(BASE_DIR, ".last_reset")

os.makedirs(FILES_DIR, exist_ok=True)

# ===== Routes =====

@app.route("/", methods=["GET"])
def index():
    files = os.listdir(FILES_DIR)
    return render_template("index.html", files=files)


@app.route("/create", methods=["POST"])
def create():
    name = request.form.get("filename", "").strip()

    # basic filename validation
    if not name or "/" in name or ".." in name:
        return redirect("/")

    path = os.path.join(FILES_DIR, name)

    if not os.path.exists(path):
        open(path, "w").close()

    return redirect("/")

@app.route("/reset", methods=["HEAD"])
def reset():
    if len(os.listdir(FILES_DIR)) == 0:
        return "", 403

    for f in os.listdir(FILES_DIR):
        os.remove(os.path.join(FILES_DIR, f))

    with open(LAST_RESET_FILE, "w") as f:
        f.write(str(time.time()))

    return "", 200

@app.route("/flag", methods=["GET"])
def flag():
    if not os.path.exists(LAST_RESET_FILE):
        return "You have to reset the files first!"

    with open(LAST_RESET_FILE) as f:
        last_reset = float(f.read())

    # window 5 seconds
    if time.time() - last_reset > 10:
        return "You have to reset the files first!"

    # 🎯 VALID SOLVE
    flag_value = open(FLAG_PATH).read()

    # 🔒 Close the game immediately
    solved_file = os.path.join(FILES_DIR, "flag")
    with open(solved_file, "w") as f:
        f.write("done\n")

    return flag_value



# ===== Run =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7878)

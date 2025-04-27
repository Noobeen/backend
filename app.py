from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from datetime import datetime

app = Flask(__name__)

CURRENT_MSG = "hello, world!"
UPDATED_AT  = datetime.utcnow()

HTML_PAGE = """<!doctype html><html><head><meta charset='utf-8'>
<title>ESP32 LCD</title></head>
<body style='font-family:sans-serif;text-align:center;margin-top:40px;'>
  <h2>Update LCD Text</h2>
  <form action='{{ url_for("set_message") }}' method='post'>
    <input name='text' maxlength='32' style='width:200px;font-size:1.2em;'>
    <button type='submit' style='font-size:1.2em;'>Send</button>
  </form>
  <p>Current message: <b>{{ current }}</b><br>Updated: {{ updated }}</p>
</body></html>"""

@app.route("/")
def home():
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    return render_template_string(HTML_PAGE, current=CURRENT_MSG,
                                  updated=UPDATED_AT.strftime("%Y-%m-%d %H:%M:%S UTC"))

@app.route("/set", methods=["POST"])
def set_message():
    global CURRENT_MSG, UPDATED_AT
    CURRENT_MSG = request.form.get("text", CURRENT_MSG)[:32]
    UPDATED_AT  = datetime.utcnow()
    return redirect(url_for("dashboard"))

@app.route("/message", methods=["GET", "POST"])
def api_message():
    """JSON API used by ESP32 (GET) and programmable clients (POST)."""
    global CURRENT_MSG, UPDATED_AT
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        CURRENT_MSG = data.get("text", CURRENT_MSG)[:32]
        UPDATED_AT  = datetime.utcnow()
        return jsonify(status="ok", text=CURRENT_MSG, updated=UPDATED_AT.isoformat())
    return jsonify(text=CURRENT_MSG, updated=UPDATED_AT.isoformat())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
import os
from flask import Flask
import main

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/clan/<clan_name>")
def go():
    clan = pick_clan(clan_name)
    return str(nm.pull_data(clan)))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

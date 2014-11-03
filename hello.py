import os
from flask import Flask
import main
import nm

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/<clan_name>")
def go(clan_name):
    clan = main.pick_clan(clan_name)
    return str(nm.pull_data(clan))

@app.route("/<clan_name>/<opt_num>")
def go2(clan_name,opt_num):
    clan = main.pick_clan(clan_name,opt_num)
    return str(nm.pull_data(clan))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
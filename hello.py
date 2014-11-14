import os
from flask import Flask, render_template, request, redirect
import main
import nm
import re
from jinja2 import evalcontextfilter, Markup, escape

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/form", methods=['POST'])
def give():
    clan = request.form['clan']
    return redirect('/clan/{0}'.format(clan))

@app.route("/home", methods=['POST'])
def home():
    return redirect('/')

@app.route("/clan/<clan_name>")
def go(clan_name):
    clan = main.pick_clan(clan_name)
    return render_template('clanpage.html', clan_name=clan_name, clan_text=main.check_clan(clan_name))

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
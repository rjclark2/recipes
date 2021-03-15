from flask import Flask, url_for, jsonify, request, Blueprint, session, redirect, render_template
import json
from serverside.serverside_table import ServerSideTable
from serverside import table_schemas
import sys

app = Flask(__name__)

with open('static/web.json') as f:
    data = json.load(f)

class TableBuilder(object):

    def collect_data_serverside(self, request):
        columns = table_schemas.SERVERSIDE_TABLE_COLUMNS
        return ServerSideTable(request, data , columns).output_result()


table_builder = TableBuilder()


@app.route("/" , methods=['GET','POST'])
def index():
    if request.method == 'POST':
        jsdata = request.get_json(force = True)
        return render_template('print.html', test = jsdata)
    else:
        return render_template("home.html")


tables = Blueprint('tables', __name__, url_prefix='/tables')


@tables.route("/serverside_table", methods=['GET','POST'])
def serverside_table_content():
    data = table_builder.collect_data_serverside(request)
    return jsonify(data)

@app.route('/pdf', methods = ['POST','GET'])
def pdf():
    global jsdata
    if request.method == 'POST':
        jsdata = request.get_json(force = True)
        out = jsdata.copy()
        out['Ingredients'] = out['Ingredients'].replace('<br/>','').replace(']',')').split('[')
        out['Instructions'] = out['Instructions'].replace('<br/>','').replace(']',')').split('[')
        return render_template('print.html', test = out)
    else:
        out = jsdata.copy()
        out['Ingredients'] = out['Ingredients'].replace('<br/>','').replace(']',')').split('[')
        out['Instructions'] = out['Instructions'].replace('<br/>','').replace(']',')').split('[')
        return render_template('print.html', test = out)

@app.route('/ngram')
def recipengram():
    return render_template('ngram.html')
@app.route('/ingredient-ngram')
def iungredientngram():
    return render_template('ing-ngram.html')
@app.route('/lengths')
def lengths():
    return render_template('lengths.html')

# Register the different blueprints
app.register_blueprint(tables)

if __name__ == '__main__':
  app.run(port=33507,debug=True)



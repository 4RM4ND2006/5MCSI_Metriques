from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

                                                                                                                                      
app = Flask(__name__)    

@app.route("/contact/")
def PageContact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/commits/")
def page_commits():
    return render_template("commits.html")
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/api/commits/")
def api_commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    commits = response.json()

    minutes = []

    for commit in commits:
        date_string = commit["commit"]["author"]["date"]
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        minutes.append(date_object.minute)

    # Compte le nombre de commits par minute
    result = Counter(minutes)

    # Format simple pour le JS
    data = []
    for minute, count in result.items():
        data.append({
            "minute": minute,
            "count": count
        })

    return jsonify(data)

  
if __name__ == "__main__":
  app.run(debug=True)

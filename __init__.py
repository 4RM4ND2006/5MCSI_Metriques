from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests

                                                                                                                                      
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
    from urllib.request import Request, urlopen
    import json
    from datetime import datetime
    from collections import Counter
    from flask import jsonify

    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    req = Request(
        url,
        headers={
            "User-Agent": "Flask-App",
            "Accept": "application/vnd.github+json"
        }
    )

    try:
        response = urlopen(req)
        commits = json.loads(response.read().decode())
    except Exception:
        return jsonify([])

    minutes = []

    for commit in commits:
        author = commit["commit"].get("author")
        if author and "date" in author:
            date_object = datetime.strptime(
                author["date"],
                "%Y-%m-%dT%H:%M:%SZ"
            )
            minutes.append(date_object.minute)

    counts = Counter(minutes)

    data = []
    for minute in range(60):
        data.append({
            "minute": minute,
            "count": counts.get(minute, 0)
        })

    return jsonify(data)


  
if __name__ == "__main__":
  app.run(debug=True)

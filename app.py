from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        cocktail_name = request.form['name']
        return search_by_name(name)
    return render_template('index.html')

def search_by_name(name):
    url = f"www.thecocktaildb.com/api/json/v1/1/search.php?s={name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['drinks']:
            return render_template('results.html', cocktails=data['drinks'])
        else:
            return render_template('error.html', message="No cocktails found.")
    else:
        return render_template('error.html', message="Failed to connect to API.")
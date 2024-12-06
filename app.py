from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the cocktail name from the form input
        cocktail_name = request.form['name']
        # Call the function to search for the cocktail and return the results
        return search_by_name(cocktail_name)
    # Render the homepage
    return render_template('index.html')

def search_by_name(name):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}"
    response = requests.get(url)

    # Check if the response from the API is successful
    if response.status_code == 200:
        try:
            data = response.json()
            # If the API returns results, render the results page
            if data['drinks']:
                return render_template('results.html', cocktails=data['drinks'])
            # Render the error page if no cocktails match the search
            else:
                return render_template('error.html', message="We couldn't find any cocktails matching your search. Try another search.")
    # Handle cases where API faces some issues
        except ValueError:
            return render_template('error.html', message="Received an unexpected response from the server. Please try again later.")
    elif response.status_code == 404:
        return render_template('error.html', message="The requested resource was not found. Please try again.")
    elif response.status_code == 500:
        return render_template('error.html', message="The server is currently experiencing issues. Please try again later.")
    else:
        return render_template('error.html', message=f"Unexpected error occurred (error {response.status_code}). Please try again later.")


if __name__ == '__main__':
    app.run(debug=True)
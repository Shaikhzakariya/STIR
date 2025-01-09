from flask import Flask, render_template, jsonify
from selenium_script import scrape_trends  # Import the scraping function

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-script', methods=['GET'])
def run_script():
    data = scrape_trends()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

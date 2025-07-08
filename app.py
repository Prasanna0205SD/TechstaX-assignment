from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)
displayed_events = []

@app.route('/')
def home():
    return render_template('index.html', events=displayed_events)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    timestamp = data.get('timestamp')

    if not timestamp:
        return {"error": "timestamp missing"}, 400

    try:
        formatted = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return {"error": "invalid timestamp format"}, 400

    if formatted not in displayed_events and formatted > datetime.utcnow():
        displayed_events.append(formatted)

    return {"status": "received"}, 200

if __name__ == '__main__':
    app.run(debug=True)
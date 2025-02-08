from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# REST endpoint that returns a JSON greeting
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, world!")

# REST endpoint that returns a JSON farewell
@app.route('/api/goodbye', methods=['GET'])
def goodbye():
    return jsonify(message="Goodbye, world!")

# Simple HTML site
@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mini Web Server</title>
    </head>
    <body>
        <h1>Welcome to the Mini Web Server</h1>
        <ul>
            <li><a href="/api/hello">Hello Endpoint</a></li>
            <li><a href="/api/goodbye">Goodbye Endpoint</a></li>
        </ul>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)
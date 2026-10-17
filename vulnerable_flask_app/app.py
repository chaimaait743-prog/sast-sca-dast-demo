import os
import subprocess
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)
# Secret lu depuis l'environnement, plus écrit en dur
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24).hex()

# Liste blanche : seules ces commandes sont autorisées
ALLOWED_COMMANDS = {
    'date': ['date'],
    'whoami': ['whoami'],
    'ls': ['ls', '-l'],
}

@app.route('/')
def index():
    return """
    <h1>Welcome to our Flask App</h1>
    <ul>
        <li><a href="/hello?name=World">Hello Page</a></li>
        <li><a href="/execute?cmd=date">Execute Command Page</a></li>
        <li><a href="/admin">Admin Area</a></li>
    </ul>
    """

@app.route('/hello')
def hello():
    name = escape(request.args.get('name', 'Guest'))  # XSS corrigé
    return f"""
    <h1>Hello Page</h1>
    <p>Hello, {name}!</p>
    <p><a href="/">Back to Homepage</a></p>
    """

@app.route('/execute')
def execute():
    key = request.args.get('cmd', 'date')
    command = ALLOWED_COMMANDS.get(key)
    if command is None:
        return "Command not allowed", 403
    result = subprocess.run(command, capture_output=True, text=True)  # plus de shell=True
    return f"""
    <h1>Execute Command Page</h1>
    <p>Executing command: <code>{escape(key)}</code></p>
    <pre>{escape(result.stdout)}</pre>
    <p><a href="/">Back to Homepage</a></p>
    """

@app.route('/admin')
def admin():
    return """
    <h1>Admin Area</h1>
    <p>Access restricted.</p>
    <p><a href="/">Back to Homepage</a></p>
    """

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')  # debug désactivé
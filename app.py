from flask import Flask
from routes import routes_bp

app = Flask(__name__)
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    # Tell Flask where to look for static files
    app.static_folder = 'static'
    app.run(debug=True)

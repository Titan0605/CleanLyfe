from flask import Flask
from app import create_app

app: Flask = create_app()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
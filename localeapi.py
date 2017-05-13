from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "You've reached locale"

if __name__ == "__main__":
    app.run()
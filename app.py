from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! This is Samiksha Nikhar. <br> I have created a Jenkins CI/CD pipeline and deployed it on an EC2 server, where this application is currently hosted. "

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

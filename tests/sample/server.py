from flask import Flask, render_template, request
app = Flask("test-container")

@app.route("/", methods=["POST"])
def home():
    data = request.get_json(force=True)
    print data
    return str(data)

app.run(port=6000)

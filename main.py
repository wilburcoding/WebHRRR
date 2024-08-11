from flask import Flask, render_template, send_file, request
app = Flask(__name__)
import os

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route('/dirs')
def dir_list():
    return os.listdir("runs")


@app.route('/img')
def get_image():
    return send_file("runs\\" + request.args.get('run') + "\\" + request.args.get('field') + "\\" + request.args.get('hour') + ".png", mimetype='image/png')
if __name__ == '__main__':
   app.run(debug=True)

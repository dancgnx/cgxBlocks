from flask import Flask, request, send_from_directory, session, jsonify, abort, make_response, render_template
from flask_cors import CORS
import cgxaux
import cloudgenix
import logging
import json
import importlib


jd= cloudgenix.jd
jd_detailed = cloudgenix.jd_detailed
log = logging.getLogger(__name__)
sess={}

# set the project root directory as the static folder, you can set others.
app = Flask(__name__ ,static_url_path="")
CORS(app)


@app.route('/exec', methods=['POST'])
def post_exec():

    #extract parameters
    input = request.json
    if not input:
        log.error("/exec missing json object")
        resp = make_response(jsonify({"message":f"JSON missing"}))
        resp.status_code = 400
        return resp

    # make sure we have the correct keys in the json
    if not all(key in input for key in ["prog"]):
        log.error("wrong json format")
        resp = make_response(jsonify({"message":f"JSON format should be: {prog}"}))
        resp.status_code = 400
        return resp
    
    # initialize
    cgx = cgxaux.CloudgenixAUX()

    # exec the program from blockly
    exec(input["prog"])

    # return the output string
    resp = make_response(jsonify({"output":cgx.out}))
    return resp
    

@app.route('/js/<path:path>')
def send_js(path):
    print(path)
    return send_from_directory(f"{app.static_folder}/js", path)


@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, send_from_directory, session, jsonify, abort, make_response
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
app = Flask(__name__ ,static_url_path="/static")
CORS(app)


@app.route('/exec', methods=['POST'])
def get_sites():

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
    

@app.route('/login', methods=['POST'])
def login():
    input = request.json
    if not input:
        log.error("/login missing json object")
        resp = make_response(jsonify({"message":f"JSON missing"}))
        resp.status_code = 400
        return resp
    if all(key in input for key in ["key","token"]):
        sess[input["key"]]={}
        sess[input["key"]]["cgx"] = cloudgenix.API()
        print(sess)
        cgx=sess[input["key"]]["cgx"]
        res = cgx.interactive.use_token(input["token"])
        if not res:
            log.error("/login Invalid token")
            resp = make_response(jsonify({"message":f"Invalid token {res}"}))
            resp.status_code = 400
            return resp
        resp = make_response(jsonify({}))
        return resp
    else:
        log.error("Can't /login json parameter error. Looking for {key:random, token:string")
        #return json.dumps({'success':False}), 400, {'ContentType':'application/json'} 
        resp = make_response(jsonify({"message":"Can't /login json parameter error. Looking for {key:random, token:string}"}))
        resp.status_code = 400
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
    
# 72c30113edf416484d4fa363f8a3041093cb31bb-pa.u.exp=1564599600000&pa.p.id=password&t.id=10000&s.id=2&pa.u.id=dan%40cloudgenix.com&o.id=15154396916390207&region=elcapitan&client_ip=54.215.252.241&session_key=P643Nr1qpXlOgkGV6gUK9zxp8cafRpofRXfV9m9Ug9Vtr9BWDTYdB2bHXRjPALTfBUsaz2E1X7pev9ygRAySbv4kfA63e2Up6qdJJugUGOUQ9tQvcrn8DjghfDzwCWsTIIuR04d9XkkSv371zTyzIuAkQoDPwlSQOLOwQ5IgiQLhbR9T6Lflfo8LUmhE44pFMeFHET4f
# <xml xmlns="http://www.w3.org/1999/xhtml"><variables><variable type="" id="w6Z|M.J3UNMr92N%!PF/">site</variable></variables><block type="cgx_token" id="^x`U?(.9#h=OP}AJ}Co!" x="153" y="58"><value name="TOKEN"><block type="text" id="CQ$GUaS=3lx-pu!ubzC-"><field name="TEXT">72c30113edf416484d4fa363f8a3041093cb31bb-pa.u.exp=1564599600000&amp;pa.p.id=password&amp;t.id=10000&amp;s.id=2&amp;pa.u.id=dan%40cloudgenix.com&amp;o.id=15154396916390207&amp;region=elcapitan&amp;client_ip=54.215.252.241&amp;session_key=P643Nr1qpXlOgkGV6gUK9zxp8cafRpofRXfV9m9Ug9Vtr9BWDTYdB2bHXRjPALTfBUsaz2E1X7pev9ygRAySbv4kfA63e2Up6qdJJugUGOUQ9tQvcrn8DjghfDzwCWsTIIuR04d9XkkSv371zTyzIuAkQoDPwlSQOLOwQ5IgiQLhbR9T6Lflfo8LUmhE44pFMeFHET4f</field></block></value><next><block type="controls_forEach" id="!p)=H{kbbCV{T+m}nSXJ"><field name="VAR" id="w6Z|M.J3UNMr92N%!PF/" variabletype="">site</field><value name="LIST"><block type="cgx_get_sites" id="6ZN}UQQyKJ3S[_/@E6;i"></block></value><statement name="DO"><block type="cgx_output" id="V%kPbl3rh,)I[b?{8!Wm"><value name="OUTPUT"><block type="variables_get" id="prQ55tEYU]cH+YcQ0p3+"><field name="VAR" id="w6Z|M.J3UNMr92N%!PF/" variabletype="">site</field></block></value></block></statement></block></next></block></xml>
from flask import request, Flask, jsonify, make_response
from recommendar import recommendar

app = Flask(__name__)
app.config["DEBUG"] = True

rec= recommendar()
print('Sucess')

@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    re =  request.get_json(force=True)
    rec.add_email(re['email'], re['account'])
    resp = make_response(jsonify(200))
    resp.headers["Content-Type"] = "text/plain"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/monthly_run', methods=['POST'])
def monthly_run():
    rec.monthly_activate()
    resp = make_response(jsonify(200))
    resp.headers["Content-Type"] = "text/plain"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
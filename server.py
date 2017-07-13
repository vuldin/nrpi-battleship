from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    #return jsonify(username='testuser', email='email', id='testid')
    if request.is_json:
        data = request.get_json()
        return jsonify(data)
    else:
        return jsonify(status="Request was not JSON")
if __name__ == '__main__':
    app.run(debug=True)

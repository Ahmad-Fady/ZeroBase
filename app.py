from flask import Flask, render_template, jsonify, request
import db_manager

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('templates/index.html')

@app.route('/offer/id')
def offer():
    return render_template('templates/item.html')

@app.route('/data', methods=['GET'])
def data_index():
    # Flask just asks the wrapper for data
    results = db_manager.get_all_data()
    return jsonify(results)

@app.route('/data', methods=['POST'])
def data_create():
    content = request.json.get('content')
    db_manager.add_entry(content)
    return jsonify({"message": "Saved!"}), 201

if __name__ == '__main__':
    # debug=True lets the server restart automatically when you save code
    app.run(debug=True)

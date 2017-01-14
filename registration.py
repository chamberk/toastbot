#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

phoneNumbers = [
    {
        'id': 1,
        'name': u'Christine', 
        'phoneNumber': u'15556667777' 
    },
    {
        'id': 2,
        'name': u'Rose',                                            
        'phoneNumber': u'18889990000' 
    }
]

@app.route('/allData', methods=['GET'])
def et_tasks():
    return jsonify({'phoneNumbers': phoneNumbers})

@app.route('/phoneNumbers', methods=['GET'])
def get_tasks():
    plist = []
    #[task for task in phoneNumbers list.append(task['phoneNumber'])
    for x in phoneNumbers:   
        plist.append(x['phoneNumber'])
    return jsonify({'phoneNumbers': plist})


from flask import abort


from flask import request

@app.route('/addPhoneNumber', methods=['POST'])
def create_task():
    if not request.json or not 'phoneNumber' in request.json:
        abort(400)
    task = {
        'id': phoneNumbers[-1]['id'] + 1,
        'name': request.json['name'],
        'phoneNumber': request.json.get('phoneNumber', ""),
    }
    phoneNumbers.append(task)
    return jsonify({'task': task}), 201



if __name__ == '__main__':
    app.run(debug=True)

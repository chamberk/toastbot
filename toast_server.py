#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import request
from twilio.rest import TwilioRestClient

app = Flask(__name__)

account_sid = "AC20bd86adfb5902d86362dcb908d40a01" # Your Account SID from www.twilio.com/console
auth_token  = "xxxxx"  # Your Auth Token from www.twilio.com/console

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

# send an sms to all phone numbers registered
@app.route('/sendsms', methods=['POST'])
def sendsms_task():
    client = TwilioRestClient(account_sid, auth_token)

    for pn in phoneNumbers:

        message = client.messages.create(body="Toast is DONE!",
            to='+'+str(pn['phoneNumber']),
            from_="+16783355213")

    return jsonify({'task': 'sms sent'}), 201


if __name__ == '__main__':
    app.run(debug=True)

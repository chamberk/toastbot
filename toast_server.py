#!flask/bin/python
from flask import Flask, jsonify,render_template, request,json
from flask import abort
from flask import request
from twilio import twiml
from twilio.rest import TwilioRestClient
import random


app = Flask(__name__)

greetings = ["hello", "hey", "yo", "hi", "what up"]
bot_greetings = ["howdy partner", "hiya pal", "hey buddy", "what's good homie?", "Good morning, Starshine. The Earth says hello!"]
bot_random = ["Start your day the toast way", "Get ready for some bomb toast", "Noms are on the way"]

account_sid = "AC20bd86adfb5902d86362dcb908d40a01" # Your Account SID from www.twilio.com/console
auth_token  = "its in slack"  # Your Auth Token from www.twilio.com/console

phoneNumbers = [
    {
        'id': 1,
        'name': u'Christine',
        'phoneNumber': u'not in slack'
    }
#    },
#    {
#        'id': 2,
#        'name': u'Rose',
#        'phoneNumber': u'18889990000'
#    }
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
    print("before adding phone number")
    if not request.json or not 'phoneNumber' in request.json:
        abort(400)
    try:
        task = {
            'id': phoneNumbers[-1]['id'] + 1,
            'name': request.json['name'],
            'phoneNumber': str(int(request.json.get('phoneNumber', ""))),
        }
        phoneNumbers.append(task)
        print("added data")
        print(task)
        return jsonify({'task': task}), 201
    except ValueError:
        abort(415)

# send an sms to all phone numbers registered
@app.route('/sendsms', methods=['POST'])
def sendsms_task():
    client = TwilioRestClient(account_sid, auth_token)

    for pn in phoneNumbers:

        message = client.messages.create(body="Toast is DONE!",
            to='+'+str(pn['phoneNumber']),
            from_="+16783355213")

    return jsonify({'task': 'sms sent'}), 201


@app.route('/toastbot', methods=['POST'])
def toastbot():
    number = request.form['From']
    message_body = request.form['Body']

    resp = twiml.Response()
    msg_final = False

    for string in greetings:
        if string in message_body:
            index = random.randrange(0, len(bot_greetings))
            resp.message(bot_greetings[index])
            msg_final = True

    if msg_final == False:
        index = random.randrange(0, len(bot_random))
        resp.message(bot_random[index])

    return str(resp)

@app.route('/deletePhoneNumber/<string:task_id>', methods=['GET'])
def delete_phone(task_id):
    print(task_id)
    task = [task for task in phoneNumbers if task['phoneNumber'] == task_id]
    print('found task')
    print(task)
    if len(task) == 0:
         abort(404)
    phoneNumbers.remove(task[0])
    return jsonify({'status': 'deleted successfully'})

@app.route('/')
def signUp():
    print request.args.get('name', "")
    print request.args.get('phoneNumber','')
    task = {
        'id': phoneNumbers[-1]['id'] + 1,
        'name': request.args.get('name', ""),
        'phoneNumber': request.args.get('phoneNumber', ""),
    }
    phoneNumbers.append(task)

    print('added phone number!')
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

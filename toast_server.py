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
bot_motivation = ["Teamwork makes the dreamwork!", "Get 'er done", "You can't have everything... Where would you put it?"]
bot_stop = "no more toast"


account_sid = "AC20bd86adfb5902d86362dcb908d40a01" # Your Account SID from www.twilio.com/console
auth_token  = "xxxx"  # Your Auth Token from www.twilio.com/console

phoneNumbers = [
    {
        'id': 1,
        'name': u'Christine',
        'phoneNumber': u'xxxx'
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
# curl -X POST  http://localhost:5000/sendsms
# curl -X POST -H "Content-Type: application/json" -d '{"message": "who wants toast"}' http://localhost:5000/sendsms
@app.route('/sendsms', methods=['POST'])
def sendsms_task():
    client = TwilioRestClient(account_sid, auth_token)

    msg = 'Toast is DONE!'
    mJson = request.get_json()
    if mJson is not None and 'message' in mJson:
        msg = mJson['message']
    for pn in phoneNumbers:

        message = client.messages.create(body=msg,
            to='+'+str(pn['phoneNumber']),
            from_="+16783355213")

    return jsonify({'task': 'sms sent'}), 201

@app.route('/toastbot', methods=['POST'])
def toastbot():
    number = request.form['From']
    message_body = request.form['Body']

    message_body = message_body.lower()

    resp = twiml.Response()
    msg_final = False

    for string in greetings:
        if string in message_body:
            index = random.randrange(0, len(bot_greetings))
            resp.message(bot_greetings[index])
            msg_final = True

    if msg_final == False and "motivate" in message_body:
        index = random.randrange(0, len(bot_motivation))
        resp.message(bot_motivation[index])
    elif msg_final == False and bot_stop in message_body:
        number = number[1:len(number)]
        delete_phone(number)
        resp.message("You are now unsubscribed from toast bot updates.")
    else:
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
    name = request.args.get('name', "")
    print name
    phoneNumber = request.args.get('phoneNumber','')
    print phoneNumber
    if len(name) and len(phoneNumber):
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

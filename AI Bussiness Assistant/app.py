from flask import Flask,render_template,request
import random
app = Flask(__name__)
intents = {
    "greetings":{
        "keywords":["hi","hello","hey"],
        "responses":['Hello! How can I assist you?',"Hi! What can I do for you?","Hello! How can I help you?"]
    },
    'services':{
        "keywords":['service','services'],
        'responses':['We offer Chatbot automation and Web Development.',"Our Services include Chatbot automation and Web Development."]
    },
    "Delivery":{
        "keywords":['delivery','time','delivery time','deliver'],
        "responses":['Project delivery time is usually 2-3 days','Delivery time depends on the project however minimum time is 2-3 days']
    },
    "pricing":{
        "keywords":['money','cost','rates','charges','price','prices','pricing'],
        'responses':['Our prices starts from $50 or depends on the project.']
    },
    'payment':{
        "keywords":['pay','payment','payment method'],
        'responses':["We accept Paypal and bank transfer.","You can use Paypal and bank transfer."]
    },
    'contacts':{
        "keywords":['contact','contacts','phone'],
        "responses":["You can contact us at: support@gmail.com","Our email is: support@gmail.com"]
    }
}
def chatbot_response(user_input):
    for intent in intents.values():
        for word in intent["keywords"]:
            if word in user_input:
                response = random.choice(intent['responses'])
                return response
    return "Please ask about Services, Delivery, Pricing, Payment and Contacts."
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/get")
def bot_response():
    user_text = request.args.get("msg")
    return chatbot_response(user_text.lower())
if __name__ == "__main__":
    app.run(debug=True)
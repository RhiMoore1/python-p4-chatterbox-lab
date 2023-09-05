from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# GET /messages: returns an array of all messages as JSON, 
# ordered by created_at in ascending order

# POST /messages: creates a new message with a body and username from params, 
# and returns the newly created post as JSON.
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    # messages = Message.query.order_by(Message.created_at)

    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at)
        messages_serialized = [
            m.to_dict() for m in messages
        ]

        response = make_response(
            jsonify(messages_serialized),
            200
        )
        return response

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body = data['body'],
            username = data['username']
        )
        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(
            jsonify(message_dict),
            201
        )
        return response




# PATCH /messages/<int:id>: updates the body of the message using params, 
# and returns the updated message as JSON.
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):

    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            jsonify(message_dict),
            200
        )
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_dict = {'message': 'record successfully deleted'}

        response = make_response(
            jsonify(response_dict),
        )





if __name__ == '__main__':
    app.run(port=5555)

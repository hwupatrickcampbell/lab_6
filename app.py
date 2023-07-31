from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

msg_counter = 0
MAX_MESSAGES = 3

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("user_choice")
def handle_user_choice(choice):
    global msg_counter
    
    if msg_counter < MAX_MESSAGES:
        msg_counter += 1
        if choice == "1":
            response = {
                "answer": "Here is the webpage to make a complaint: ",
                "url": url_for("static", filename="complaint.html"),
            }
        elif choice == "2":
            response = {
                "answer": "Here is the webpage to find out about the status of a current order: ",
                "url": url_for("static", filename="status.html"),
            }
        elif choice == "3":
            response = {
                "answer": "Here is the webpage to ask a about a specific product: ",
                "url": url_for("static", filename="product.html"),
            }
        else:
            response = {"answer": "Choose again", "url": None}

        message = f"{response['answer']}<a href='{response['url']}'>{response['url']}</a>"
        emit("bot_response", {"message": message})
    
    if msg_counter == MAX_MESSAGES:
        emit("bot_response", {"message": "Thank you for using the service. The chat session is now closed."})
        emit("close_connection")
        msg_counter = 0

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=8000)

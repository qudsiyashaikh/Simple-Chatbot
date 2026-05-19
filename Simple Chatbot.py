from flask import Flask, render_template_string, request, session

app = Flask(__name__)
app.secret_key = 'chatbot_secret_key'

# --- HTML & CSS TEMPLATE ---
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eceff1; text-align: center; margin-top: 40px; }
        .chat-container { display: inline-block; padding: 20px; background: white; border-radius: 10px; box-shadow: 0px 0px 15px rgba(0,0,0,0.1); width: 450px; text-align: left; }
        h2 { text-align: center; color: #37474f; }
        .chat-box { width: 100%; height: 300px; border: 1px solid #cfd8dc; border-radius: 5px; overflow-y: auto; padding: 10px; box-sizing: border-box; background: #fafafa; margin-bottom: 15px; }
        .msg { margin: 8px 0; padding: 10px; border-radius: 8px; max-width: 80%; word-break: break-word; }
        .user-msg { background: #b3e5fc; margin-left: auto; text-align: right; color: #01579b; }
        .bot-msg { background: #cfd8dc; color: #263238; }
        .input-area { display: flex; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #cfd8dc; border-radius: 5px 0 0 5px; font-size: 16px; }
        button { padding: 10px 20px; background-color: #0086c3; color: white; border: none; font-weight: bold; border-radius: 0 5px 5px 0; cursor: pointer; }
        button:hover { background-color: #005b9f; }
    </style>
</head>
<body>

<div class="chat-container">
    <h2>🤖 Simple Chatbot</h2>
    
    <!-- Chat Window containing Inputs and Outputs -->
    <div class="chat-box">
        {% for chat in chat_history %}
            <div class="msg user-msg"><strong>You:</strong> {{ chat.user }}</div>
            <div class="msg bot-msg"><strong>Bot:</strong> {{ chat.bot }}</div>
        {% endfor %}
    </div>

    <form method="POST" class="input-area">
        <input type="text" name="user_message" placeholder="Type 'hello', 'how are you', or 'bye'..." required autofocus>
        <button type="submit">Send</button>
    </form>
</div>

</body>
</html>
"""

# --- NLP BASICS / PRE-DEFINED RESPONSES ---
def get_bot_reply(user_text):
    # NLP Basics: Text normalization (Lowercasing input to handle variations)
    text = user_text.lower().strip()
    
    # Conditions Concept: Finding matching rules for structured responses
    if "hello" in text or "hi" in text:
        return "Hello! I am your simple Flask chatbot. How can I assist you today?"
    elif "how are you" in text:
        return "I am doing great, thank you for asking! What about you?"
    elif "name" in text:
        return "I am a simple automated script running on a Flask webserver."
    elif "bye" in text or "exit" in text:
        return "Goodbye! Have a wonderful day ahead!"
    else:
        return "I am sorry, I can only understand basic keywords like 'hello', 'name', 'how are you', or 'bye'."


@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        user_msg = request.form.get('user_message')
        bot_reply = get_bot_reply(user_msg)
        
        # Updating local session memory to retain conversation workflow
        history = session['history']
        history.append({"user": user_msg, "bot": bot_reply})
        session['history'] = history

    return render_template_string(HTML, chat_history=session['history'])

if __name__ == '__main__':
    app.run(debug=True)
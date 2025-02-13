from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Home page'

@app.route('/form')
def form():
    return render_template('formulario.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    bot_response = chatbot.get_response(user_message)  # Obtén la respuesta del chatbot
    return jsonify({'response': bot_response})

@app.route('/cube')
def cubeR():
    return render_template('cube.html')

try:
    if __name__ == '__main__':
        app.run(host='192.168.1.7', port=5000, debug=True)
except Exception as e:
    print(f'Error: {e}')
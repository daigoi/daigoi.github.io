from flask import Flask, request, render_template, jsonify, send_file, json
from text_processor2 import process_received_text
from text_processor2 import get_dialogue_history
from flask_cors import CORS
from flask_socketio import SocketIO
from text_processor2 import process_received_text, get_dialogue_history, initialize_text_processor

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


received_texts = []


@app.route('/')
def index():
    return render_template('voice_recognition.html')

@app.route('/send_text', methods=['POST'])
def send_text():
    text = request.form['text']
    received_texts.append(text)
    print("自分: " + text)
    
    process_received_text(text)

    return 'OK', 200

@app.route('/texts')
def texts():
    return jsonify(received_texts)

@app.route('/get_history')
def get_history():
    history = get_dialogue_history()
    return json.dumps(history, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/get_audio')
def get_audio():
    return send_file("output.wav", mimetype="audio/wav")

@app.route('/output.wav')
def output_wav():
    return send_file("output.wav", mimetype='audio/wav')

initialize_text_processor(socketio)
if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, host='0.0.0.0', port=5000)
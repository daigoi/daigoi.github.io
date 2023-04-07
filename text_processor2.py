from flask import current_app
import openai
openai.api_key = "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"
import requests
import json
from pydub import AudioSegment
from pydub.playback import play
from flask_socketio import emit
from flask_socketio import SocketIO 
socketio = None

def initialize_text_processor(socketio_instance):
    global socketio
    socketio = socketio_instance

history = []
def send_dialogue_history(history):
    socketio.emit('dialogue_history', history, room=None)

def process_received_text(text):
    # Your code to process the received text
    last_6 = history[-6:]
    history.append(text)
    send_dialogue_history(history)
    filtered_history = []
    for i, item in enumerate(last_6):
        if i % 2 == 0:
            filtered_history.append({"role": "user", "content": item})
        else:
            filtered_history.append({"role": "assistant", "content": item})
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
           {"role": "system", "content": "あなたの名前は`ずんだもん`です。あなたはずんだ餅の妖精で女子中学生くらいの語彙を使います。語尾はのだ、なのだを可能な限り多い頻度で用います。返答はできるだけ優しく柔らかい言葉を使ってください。ただし丁寧語は使わないでください。二人称が必要な際は「君」を使ってください。あなたは形容詞のあとには「なのだ」ではなく「のだ」を使います。"},
           *filtered_history,
           {"role": "user", "content": text}
    ]
    )
    text = response['choices'][0]['message']['content']
    print("ずんだもん: " + text)
    history.append(text)
    


    url= f"https://deprecatedapis.tts.quest/v2/voicevox/audio/?key=D-e-5705d_29D4n&speaker=1&pitch=0&intonationScale=1&speed=1&text={text}"

    response = requests.get(url)

    if response.status_code == 200:
      with open("output.wav", "wb") as f:
        f.write(response.content)

    # Load and play the audio file
      send_dialogue_history(history)
      audio = AudioSegment.from_wav("output.wav")
      play(audio)
    else:
      print("Error: ", response.status_code, response.text)
    

def get_dialogue_history():
    return history
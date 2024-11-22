from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import crash_lang as cr
import openai
import os
from openai import OpenAI
import speech_recognition as sr

app = Flask(__name__)
CORS(app)

client = OpenAI()

# 초기 대화 기록 설정
conversation_history = [{"role": "system", "content": "Hello! How can I help you today?"}]

# 음성 인식 함수
def recognize_speech(micindex, result):
    try:
        question = cr.google_free(micindex)
        result.append(question)
    except Exception as e:
        print(f"Error during speech recognition: {e}")
        result.append(None)

# Flask 서버 엔드포인트
@app.route('/api/chat', methods=['GET'])
def chat():
    micindex = request.json.get('micindex', 6)  # POST 요청에서 micindex를 가져옴, 기본값은 6으로 설정

    result = []
    recognition_thread = threading.Thread(target=recognize_speech, args=(micindex, result))
    recognition_thread.start()
    recognition_thread.join()

    question = result[0]
    if question is None:
        return jsonify({'error': 'Voice not recognized or API error'}), 400

    # 사용자의 질문을 대화 기록에 추가
    conversation_history.append({"role": "user", "content": question})
    
    # GPT-3.5-turbo 모델을 사용해 응답을 생성
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        answer = completion.choices[0].message.content

        # 생성된 응답을 대화 기록에 추가
        conversation_history.append({"role": "assistant", "content": answer})

        return jsonify({'answer': answer})

    except Exception as e:
        print(f"Can't access API; {e}")
        return jsonify({'error': str(e)}), 500

# 음성 인식을 별도의 스레드에서 실행하는 함수
def start_voice_recognition(micindex):
    while True:
        result = []
        recognize_speech(micindex, result)
        question = result[0]
        if question:
            print(f"Recognized voice input: {question}")
            # 대화 기록에 추가
            conversation_history.append({"role": "user", "content": question})

if __name__ == '__main__':
    # 음성 인식을 별도의 스레드에서 실행
    micindex = 6  # 기본 micindex 설정
    voice_thread = threading.Thread(target=start_voice_recognition, args=(micindex,))
    voice_thread.daemon = True
    voice_thread.start()

    # Flask 서버를 메인 스레드에서 실행
    app.run(debug=True)

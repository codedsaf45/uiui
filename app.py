from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI()

# 초기 대화 기록 설정
conversation_history = [{"role": "system", "content": "Hello! How can I help you today?"}]

@app.route('/api/send_response', methods=['POST'])
def send_response():
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    question = data['text']
    print(f"Received question: {question}")

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

        # 응답을 반환
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"Can't access API; {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

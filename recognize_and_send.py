import requests
import crash_lang as cr

def recognize_and_send(micindex=6):
    while True:
        question = cr.google_free(micindex)
        if question:
            print(f"Recognized voice input: {question}")

            # Flask 서버로 OpenAI API 요청을 보냄
            response = requests.post("http://127.0.0.1:5000/api/send_response", json={"text": question})
            
            if response.status_code == 200:
                server_response = response.json().get('answer')
                print("OpenAI response:", server_response)

                # 필요하다면 이 응답을 프론트엔드로 POST 요청 전송
                # 프론트엔드 서버 주소를 'http://frontend-server-url'로 변경
                frontend_response = requests.post("http://frontend-server-url/api/display", json={"response": server_response})
                print("Sent to frontend:", frontend_response.status_code)
            else:
                print("Error from Flask server:", response.json().get('error'))

if __name__ == '__main__':
    recognize_and_send()

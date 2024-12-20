async function getGptOutput() {
    const response = await fetch('http://127.0.0.1:8000/gptOutput', {
      method: 'POST'
    });
    const data = await response.json();
    console.log("GPT Response:", data.gptresponse);
    document.getElementById('response').innerText = data.response;
  }
  
  async function getUserInput() {
    const response = await fetch('http://127.0.0.1:8000/UserInput', {
      method: 'POST'
    });
    const data = await response.json();
    console.log("User Message:", data.usermessage);
    document.getElementById('response').innerText = data.response;
  }   
  
  // 함수 호출 추가
  getGptOutput();
  getUserInput();
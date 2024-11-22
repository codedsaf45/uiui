const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_IMG = "https://cdn.newshyu.com/news/photo/202206/1006285_213255_552.jpg";
const PERSON_IMG = "https://cdn2.unrealengine.com/18br-headband-cosmetics-naruto-toast-400x400-5228564ee685.jpg";
const BOT_NAME = "나중에 이미지 로컬 이미지로 바꿔라";
const PERSON_NAME = "rapidfire";

msgerForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const msgText = "";
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";

  await botResponse(msgText);
});

// 이건 메시지를 프론트엔드에 표시하는 함수
function appendMessage(name, img, side, text) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}
// 이건 응답을 받는 합수들
async function sendUserInput() {
  const response = await fetch('http://127.0.0.1:8000/UserInput', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({}),
  });

  const data = await response.json();
  const userMessage = data.usermessage;
  
  console.log("User Message:", data.usermessage);
  appendMessage(PERSON_NAME, PERSON_IMG, "right", userMessage);

  
}

async function sendGptOutput() {
  const response = await fetch('http://127.0.0.1:8000/gptOutput', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({}),
  });

  const data = await response.json();
  const botMessage = data.gptresponse;
  console.log("GPT Response:", data.gptresponse);
  appendMessage(BOT_NAME, BOT_IMG, "left", botMessage);
  
}

/*
// 이건 백엔드 서버에 메시지를 보내고 응답을 받는 함수
async function botResponse(userMessage) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userMessage }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    const botMessage = data.response;
    const delay = botMessage.split(" ").length * 100;

    setTimeout(() => {
      appendMessage(BOT_NAME, BOT_IMG, "left", botMessage);
    }, delay);
  } catch (error) {
    console.error("Error during bot response:", error);
    appendMessage(BOT_NAME, BOT_IMG, "left", "Sorry, I couldn't get a response. Please try again later.");
  }
}
*/












// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}
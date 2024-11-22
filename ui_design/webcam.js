document.getElementById('camera').addEventListener('click', async () => {
    try {
        // 웹캠 스트림 요청
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });

        // HTML 비디오 요소 가져오기
        const videoElement = document.getElementById('webcam');
        
        // 스트림을 비디오 요소에 연결
        videoElement.srcObject = stream;

        // 비디오 요소 보이기
        videoElement.style.display = 'block';
    } catch (error) {
        // 에러 처리
        console.error("웹캠에 접근할 수 없습니다:", error);
        alert("웹캠에 접근할 수 없습니다. 권한을 확인해주세요.");
    }
});
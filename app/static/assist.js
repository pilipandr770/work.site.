document.addEventListener("DOMContentLoaded", function() {
    const btn = document.getElementById("chat-open-btn");
    const chatWindow = document.getElementById("chat-window");
    const chatInput = document.getElementById("chat-input");
    const chatSend = document.getElementById("chat-send");
    const chatMin = document.getElementById("chat-minimize");
    const chatExpand = document.getElementById("chat-expand");
    const chatMessages = document.getElementById("chat-messages");
    let expanded = false;

    // Відкрити чат
    btn.onclick = () => {
        chatWindow.style.display = "flex";
        chatWindow.style.width = "340px";
        chatWindow.style.height = "420px";
        chatWindow.style.right = "30px";
        chatWindow.style.bottom = "90px";
        expanded = false;
        setTimeout(() => chatInput.focus(), 100);
    };
    // Надіслати повідомлення кнопкою
    chatSend.onclick = sendMessage;
    // Надіслати Enter'ом
    chatInput.onkeydown = function(e) {
        if (e.key === "Enter") sendMessage();
    };
    // Згорнути чат
    chatMin.onclick = () => {
        chatWindow.style.display = "none";
    };
    // Розгорнути/зменшити чат
    chatExpand.onclick = () => {
        if (!expanded) {
            chatWindow.style.width = "95vw";
            chatWindow.style.height = "90vh";
            chatWindow.style.right = "2vw";
            chatWindow.style.bottom = "2vh";
            expanded = true;
        } else {
            chatWindow.style.width = "340px";
            chatWindow.style.height = "420px";
            chatWindow.style.right = "30px";
            chatWindow.style.bottom = "90px";
            expanded = false;
        }
    };

    // Надсилання повідомлення
    function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        appendMessage("user", message);
        chatInput.value = "";
        chatInput.focus();

        fetch('/assist/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message})
        })
        .then(resp => resp.json())
        .then(data => appendMessage("bot", data.reply))
        .catch(() => appendMessage("bot", "Помилка звʼязку з сервером 😥"));
    }

    // Вивід повідомлення в чат
    function appendMessage(who, text) {
        const div = document.createElement("div");
        div.className = who;
        div.textContent = text;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});

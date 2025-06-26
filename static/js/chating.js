// chat-widget.js
(function () {
    // إنشاء عناصر الزر والنافذة
    const chatButton = document.createElement('div');
    chatButton.id = 'chat-button';
    chatButton.innerHTML = '<br>&Tab;&Tab;<i class="fas fa-comment-dots"></i>';

    const chatContainer = document.createElement('div');
    chatContainer.id = 'chat-container';
    chatContainer.innerHTML = `
    <div class="chat-header">
    <h5>Chat</h5>
    <button id="close-chat" class="btn btn-sm btn-danger">
    <i class="fas fa-times"></i>
    </button>
    </div>
    <div class="chat-body" id="chatBody">
    <!-- الرسائل ستظهر هنا -->
    </div>
    <div class="chat-footer">
    <form class="d-flex" id="messageForm">
    <input type="text" class="form-control me-2" placeholder="اكتب رسالة..." id="messageInput" name="prompt">
    <button type="submit" class="btn btn-success">إرسال</button>
    </form>
    </div>
    `;

    // إلحاق العناصر إلى الـ body
    document.body.appendChild(chatButton);
    document.body.appendChild(chatContainer);

    // الحصول على المراجع للعناصر
    const chatBody = document.getElementById('chatBody');
    const messageForm = document.getElementById('messageForm');
    const messageInput = document.getElementById('messageInput');
    const closeChatButton = document.getElementById('close-chat');
    const chatHeader = chatContainer.querySelector('.chat-header');

    // دالة للحصول على الوقت الحالي بتنسيق HH:MM
    function getCurrentTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    // دالة لإضافة رسالة إلى نافذة الدردشة
    function addMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', type);

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        avatarDiv.textContent = type === 'sent' ? 'U': 'A'; // U للمستخدم، A للذكاء الاصطناعي

        const messageBubbleDiv = document.createElement('div');
        messageBubbleDiv.classList.add('message-bubble');
        messageBubbleDiv.innerHTML = message;

        const timestampDiv = document.createElement('div');
        timestampDiv.classList.add('timestamp');
        timestampDiv.textContent = getCurrentTime();

        // ترتيب العناصر بناءً على نوع الرسالة
        if (type === 'sent') {
            messageDiv.appendChild(messageBubbleDiv);
            messageDiv.appendChild(avatarDiv);
        } else {
            messageDiv.appendChild(avatarDiv);
            messageDiv.appendChild(messageBubbleDiv);
        }
        messageDiv.appendChild(timestampDiv);

        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
        // حفظ المحادثة بعد إضافة كل رسالة
        saveMessages();
    }

    // دالة لمحاكاة رد الذكاء الاصطناعي مع تأخير عشوائي
    async function getAIResponse(userMessage) {
        let mypost = document.getElementById('messageForm');
        let myform = new FormData(mypost);
        fetch('/ask', {
            method: 'POST',
            body: myform
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text;
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            asert('Error:', error);
        });
        return data
    }

    // حفظ الرسائل في localStorage
    function saveMessages() {
        localStorage.setItem('ChatMessages',
            chatBody.innerHTML);
    }

    // تحميل الرسائل من localStorage عند فتح الصفحة
    function loadMessages() {
        const saved = localStorage.getItem('ChatMessages');
        if (saved) {
            chatBody.innerHTML = saved;
        }
    }

    // تحميل الرسائل عند بدء التشغيل
    //loadMessages();

    // التعامل مع إرسال الرسائل عند تقديم النموذج
    messageForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const userMessage = messageInput.value.trim();
        messageInput.value = '';
        if (userMessage !== '') {
            addMessage(userMessage, 'sent');
            //const aiResponse = await getAIResponse(userMessage);
            //addMessage(aiResponse, 'received');
            let mypost = document.getElementById('messageForm');
            let myform = new FormData();
            myform.append('prompt', userMessage)
            fetch('/ask', {
                method: 'POST',
                body: myform
            })
            .then(response => {
                return response.json()
            }) // Parse JSON (returns a Promise)
            .then(data => {
                addMessage(String(data.ans), 'received'); // Now `data` is the parsed JSON
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage('Failed to get response', 'received');
            });
        }
    });

    // دعم إرسال الرسائل بالضغط على زر Enter بدون الانتظار للنموذج
    messageInput.addEventListener('keydown',
        function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                messageForm.dispatchEvent(new Event('submit'));
            }
        });

    chatContainer.classList.add('open');
    // إظهار النافذة عند النقر على زر الدردشة
    chatButton.addEventListener('click',
        () => {
            chatButton.style.display = 'None';
            chatContainer.style.display = 'block';
        });

    // إخفاء النافذة عند النقر على زر الإغلاق
    closeChatButton.addEventListener('click',
        () => {
            chatContainer.style.display = 'None';
            chatButton.style.display = 'block';
        });

    // جعل النافذة قابلة للسحب عبر رأس الدردشة فقط
    let isDragging = false;
    let offsetX, offsetY;

    chatHeader.style.cursor = 'move';

    chatHeader.addEventListener('mousedown',
        (e) => {
            isDragging = true;
            offsetX = e.clientX - chatContainer.getBoundingClientRect().left;
            offsetY = e.clientY - chatContainer.getBoundingClientRect().top;
        });

    document.addEventListener('mousemove',
        (e) => {
            if (!isDragging) return;
            const x = e.clientX - offsetX;
            const y = e.clientY - offsetY;
            chatContainer.style.left = `${x}px`;
            chatContainer.style.top = `${y}px`;
            chatContainer.style.right = 'auto';
            chatContainer.style.bottom = 'auto';
        });

    document.addEventListener('mouseup',
        () => {
            isDragging = false;
        });

    // حفظ المحادثة قبل إغلاق الصفحة
    window.addEventListener('beforeunload',
        saveMessages);

    // إضافة CSS للصفحة
    const style = document.createElement('style');
    style.textContent = `
    /* زر الدردشة */
    #chat-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #075E54;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    z-index: 1001;
    transition: transform 0.3s ease, opacity 0.3s ease;
    }

    #chat-button:hover {
    transform: scale(1.05);
    }

    #chat-button.hidden {
    opacity: 0;
    pointer-events: none;
    }

    /* نافذة الدردشة */
    #chat-container {
    position: fixed;
    bottom: -450px;
    right: 20px;
    width: 350px;
    height: 450px;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    z-index: 1000;
    transition: bottom 0.3s ease-in-out;
    }

    #chat-container.open {
    bottom: 20px;
    }

    /* رأس الدردشة */
    .chat-header {
    background-color: #075E54;
    color: white;
    padding: 10px;
    text-align: center;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    }

    /* جسم الدردشة */
    .chat-body {
    height: 330px;
    overflow-y: auto;
    padding: 10px;
    background-color: #ECE5DD;
    }

    /* الرسائل */
    .chat-message {
    display: flex;
    align-items: flex-end;
    margin-bottom: 10px;
    }

    .chat-message.sent {
    justify-content: flex-end;
    }

    .chat-message.received {
    justify-content: flex-start;
    }

    .avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin: 0 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    color: white;
    }

    .message-bubble {
    padding: 10px;
    border-radius: 15px;
    max-width: 70%;
    position: relative;
    background-color: white;
    color: black;
    }

    /* Styling for code blocks in messages */
    .message-bubble pre {
    background-color: #f5f5f5;
    border-radius: 4px;
    padding: 8px;
    overflow-x: auto;
    direction: ltr;
    text-align: left;
    }

    .message-bubble code {
    font-family: monospace;
    background-color: #f5f5f5;
    padding: 2px 4px;
    border-radius: 3px;
    color: #333;
    }

    /* Ensure RTL/LTR spans are properly styled */
    .message-bubble span[dir="rtl"] {
    direction: rtl;
    unicode-bidi: embed;
    }

    .message-bubble span[dir="ltr"] {
    direction: ltr;
    unicode-bidi: embed;
    }

    .timestamp {
    font-size: 0.7rem;
    color: #777;
    margin-top: 2px;
    }

    /* ذيل الدردشة */
    .chat-footer {
    padding: 10px;
    background-color: #f1f1f1;
    }
    `;
    document.head.appendChild(style);
})();
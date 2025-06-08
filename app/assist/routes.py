import openai
from flask import Blueprint, request, jsonify
import os
import time

assist_bp = Blueprint('assist', __name__)

@assist_bp.route('/assist/chat', methods=['POST'])
def assist_chat():
    data = request.json
    user_message = data.get('message', '')

    api_key = os.getenv('OPENAI_API_KEY')
    assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
    openai.api_key = api_key

    try:
        # 1. Створити thread
        thread = openai.beta.threads.create()
        thread_id = thread.id

        # 2. Додати повідомлення
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )

        # 3. Запустити асистента
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # 4. Дочекатися завершення run
        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == "completed":
                break
            time.sleep(1)

        # 5. Отримати відповідь
        messages = openai.beta.threads.messages.list(thread_id=thread_id)
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                reply = msg.content[0].text.value
                return jsonify({"reply": reply})
        return jsonify({"reply": "Асистент не відповів."})
    except Exception as e:
        return jsonify({"reply": f"Помилка: {str(e)}"}), 500

from __future__ import annotations

from flask import Flask, render_template, request, jsonify
import secrets

app = Flask(__name__)

MIN_LEN = 16
MAX_LEN = 20
DEFAULT_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:,.?/"

def generate_passwords(charset: str, length: int, count: int = 20) -> list[str]:
    # Генерация криптографически стойкая (secrets)
    return ["".join(secrets.choice(charset) for _ in range(length)) for _ in range(count)]

@app.get("/")
def index():
    return render_template("index.html", default_charset=DEFAULT_CHARSET, min_len=MIN_LEN, max_len=MAX_LEN)

@app.post("/api/generate")
def api_generate():
    data = request.get_json(silent=True) or {}
    charset = (data.get("charset") or "").strip()
    length = data.get("length")

    if not charset:
        return jsonify({"error": "Введите хотя бы один символ для генерации."}), 400

    # Убираем дубликаты символов, сохраняя порядок (удобнее и предсказуемее)
    # Если хочешь учитывать дубликаты как "вес", просто удали этот блок.
    unique_charset = "".join(dict.fromkeys(charset))

    if not isinstance(length, int):
        return jsonify({"error": "Некорректная длина пароля."}), 400

    if length < MIN_LEN or length > MAX_LEN:
        return jsonify({"error": f"Длина должна быть от {MIN_LEN} до {MAX_LEN}."}), 400

    passwords = generate_passwords(unique_charset, length, count=20)
    return jsonify({"passwords": passwords})

if __name__ == "__main__":
    # Запуск: http://127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=True)
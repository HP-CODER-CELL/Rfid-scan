from flask import Flask, render_template_string, jsonify
import threading
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

app = Flask(__name__)
reader = SimpleMFRC522()

last_tag_info = {"id": None, "text": None, "timestamp": None}

# Background thread to continuously read RFID
def rfid_reader_loop():
    global last_tag_info
    while True:
        try:
            id, text = reader.read()
            print(f"Detected: ID={id}, Text={text}")
            last_tag_info = {
                "id": id,
                "text": text,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            time.sleep(1)  # avoid too-fast looping
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

# HTML template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>RFID Movements</title>
  <meta http-equiv="refresh" content="5">
  <style>
    body { font-family: Arial; padding: 20px; }
    h1 { color: #333; }
  </style>
</head>
<body>
  <h1>RFID Movement Log</h1>
  {% if id %}
    <p><strong>Last Detected ID:</strong> {{ id }}</p>
    <p><strong>Text:</strong> {{ text }}</p>
    <p><strong>Timestamp:</strong> {{ timestamp }}</p>
  {% else %}
    <p>No tag detected yet.</p>
  {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE, **last_tag_info)

@app.route('/api/latest')
def api_latest():
    return jsonify(last_tag_info)

if __name__ == '__main__':
    # Start RFID reader in background
    threading.Thread(target=rfid_reader_loop, daemon=True).start()
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()

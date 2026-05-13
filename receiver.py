import socket
import json
import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

UDP_IP = "0.0.0.0" 
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False) 


i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

button = digitalio.DigitalInOut(board.D17)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP 

font = ImageFont.load_default()

current_mode = 0  
button_prev_state = True
received_data = {"cpu_usage": 0, "memory_usage": 0, "spotify_track": "-", "spotify_artist": "-"}

print(f"受信待機中... Port: {UDP_PORT}")

try:
    while True:
        if not button.value and button_prev_state:
            current_mode = 1 if current_mode == 0 else 0
            print(f"モード切り替え: {current_mode}")
        button_prev_state = button.value

        try:
            data, addr = sock.recvfrom(1024)
            received_data = json.loads(data.decode('utf-8'))
        except BlockingIOError:
            pass 
        except Exception as e:
            print(f"受信エラー: {e}")

        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)

        if current_mode == 0:
            draw.text((0, 0), "=== PC Monitor ===", font=font, fill=255)
            draw.text((0, 20), f"CPU: {received_data.get('cpu_usage', 0)} %", font=font, fill=255)
            draw.text((0, 40), f"MEM: {received_data.get('memory_usage', 0)} %", font=font, fill=255)
        else:
            draw.text((0, 0), "=== Spotify ===", font=font, fill=255)
            draw.text((0, 20), f"Tr: {received_data.get('spotify_track', '')[:15]}", font=font, fill=255)
            draw.text((0, 40), f"Ar: {received_data.get('spotify_artist', '')[:15]}", font=font, fill=255)

        oled.image(image)
        oled.show()

        time.sleep(0.1) 

except KeyboardInterrupt:
    print("\n終了します。")
    oled.fill(0)
    oled.show()
    sock.close()

import socket
import json
import time
import psutil
# import spotipy 

# ラズパイ側のIPアドレスとポート番号を設定
UDP_IP = "192.168.1.xxx" # 
UDP_PORT = 5005

print(f"UDP送信先 IP: {UDP_IP} / Port: {UDP_PORT}")

# UDP通信用のソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        # 1. PCのシステム情報を取得
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()

        # 2. Spotifyの情報を取得
  
        current_track = "Test Track"
        current_artist = "Test Artist"


        data = {
            "cpu_usage": cpu_percent,
            "memory_usage": mem.percent,
            "spotify_track": current_track,
            "spotify_artist": current_artist
        }


        message = json.dumps(data).encode('utf-8')
        sock.sendto(message, (UDP_IP, UDP_PORT))

        print(f"送信完了: {data}")
        time.sleep(2) #

except KeyboardInterrupt:
    print("\n通信を終了します。")
    sock.close()

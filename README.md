wireless-sub-monitor

Raspberry Pi 3とSpotify APIを活用した簡易的なワイヤレスサブモニターのプログラムです。

概要
PCのシステム情報（CPU/メモリ使用率）およびSpotifyの再生情報を取得し、UDP通信でRaspberry Piへ送信します。
Raspberry Pi側では受信したデータをOLEDディスプレイに表示し、タクトスイッチで表示モードの切り替えを行います。

システム構成
- 送信側 (PC): Python (psutil) -> UDP送信
- 受信側 (Raspberry Pi 3): Python -> UDP受信 -> I2C (OLEDディスプレイ) / GPIO (タクトスイッチ)

ファイル構成
- `pc_sender.py`: PC側で実行し、各種情報をUDPで送信するスクリプト。
- `pi_receiver.py`: Raspberry Pi側で実行し、データを受信してOLEDに描画するスクリプト。

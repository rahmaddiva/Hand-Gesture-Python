# Hand Gesture Recognition with Video Trigger

Proyek ini mendeteksi beberapa gesture tangan dan facepalm menggunakan webcam, lalu memutar video beserta audio sesuai gesture yang terdeteksi.

## Fitur

- Deteksi gesture:
  - Fist up (kepalkan tangan lalu gerakkan ke atas): memutar `video1.mp4`
  - Facepalm (tangan ke wajah): memutar `video2.mp4`
  - Metal/Rock sign (telunjuk & kelingking terbuka): memutar `video3.mp4`
  - Salute/kebingungan (tangan ke dahi): memutar `video3.mp4` (opsional)
- Video dan audio diputar secara sinkron menggunakan OpenCV + pygame

## Struktur File

```
hand_gesture/
├── main.py
├── videos/
│   ├── video1.mp4
│   ├── video1_audio.mp3
│   ├── video2.mp4
│   ├── video2_audio.mp3
│   ├── video3.mp4
│   └── video3_audio.mp3
└── README.md
```

## Instalasi

1. Aktifkan virtual environment (opsional tapi direkomendasikan):
   ```powershell
   .venv\Scripts\activate
   ```
2. Install dependensi:
   ```powershell
   pip install opencv-python mediapipe pygame numpy
   ```

## Cara Menjalankan

1. Pastikan file video dan audio sudah ada di folder `videos/`.
2. Jalankan script:
   ```powershell
   python main.py
   ```
3. Ikuti instruksi gesture di terminal. Jika gesture terdeteksi, video dan audio akan diputar.
4. Tekan `q` pada jendela kamera untuk keluar.

## Kustomisasi Gesture

- Untuk menambah gesture baru, buat fungsi deteksi baru di `main.py` dengan menganalisa posisi landmark tangan/wajah.
- Tambahkan pemanggilan fungsi tersebut di main loop dan tentukan aksi yang diinginkan.

## Catatan

- Untuk deteksi facepalm, diperlukan webcam yang cukup jelas dan pencahayaan baik.
- Jika audio tidak muncul, pastikan file mp3 tersedia dan pygame terinstall dengan benar.

## Lisensi

MIT License
"# Hand-Gesture-Python"

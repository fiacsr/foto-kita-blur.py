import cv2
from cvzone.HandTrackingModule import HandDetector
import time

# Inisialisasi Kamera
cap = cv2.VideoCapture(0)

# Inisialisasi Pendeteksi Tangan (deteksi minimal 80% agar akurat)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Variabel Waktu Blur
blur_until = 0
blur_duration = 1  # Detik

print("Program berjalan dengan CVZone. Angkat jari PEACE!")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Balik kamera biar seperti cermin
    frame = cv2.flip(frame, 1)

    # Temukan tangan (draw=True untuk memunculkan garis tangan, ubah False jika ingin bersih)
    hands, frame = detector.findHands(frame, draw=True)

    peace_detected = False

    if hands:
        hand = hands[0]
        # detector.fingersUp() akan mengembalikan list [jempol, telunjuk, tengah, manis, kelingking]
        # Nilai 1 berarti tegak, 0 berarti menekuk
        fingers = detector.fingersUp(hand)

        # Logika Peace: Jempol(0/1 bebas), Telunjuk(1), Tengah(1), Manis(0), Kelingking(0)
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            peace_detected = True

    # Manajemen Waktu Efek Blur
    current_time = time.time()
    if peace_detected:
        blur_until = current_time + blur_duration

    if current_time < blur_until:
        # Berikan efek blur
        frame = cv2.GaussianBlur(frame, (99, 99), 0)
        cv2.putText(frame, "foto kita blur", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Tampilkan ke layar
    cv2.imshow("Peace Gesture Blur", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import pygame
import numpy as np
import math

# ========== VIDEO PLAYER (OPENCV + PYGAME + AUDIO) ==========
def play_video(video_path):
    pygame.init()
    pygame.display.set_caption("Video Player")

    DISPLAY_WIDTH = 720
    DISPLAY_HEIGHT = 480

    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Gagal membuka video!")
        return

    # AUDIO MP3 (hasil ekstraksi)
    import os
    audio_path = video_path.replace(".mp4", "_audio.mp3")
    if os.path.exists(audio_path):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Audio gagal diputar: {e}")
    else:
        print("Audio tidak ditemukan, video tetap diputar tanpa suara.")

    clock = pygame.time.Clock()
    running = True

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()

        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        clock.tick(30)

    cap.release()
    pygame.mixer.music.stop()
    pygame.quit()


# ========== HAND GESTURE + FACE MESH DETECTION ==========
mpHands = mp.solutions.hands
mpFace = mp.solutions.face_mesh

hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
face_mesh = mpFace.FaceMesh(max_num_faces=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils


def euclidean_distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


# ========== FACEPALM DETECTION ==========
def is_facepalm(hands_result, face_result):
    if not (hands_result.multi_hand_landmarks and face_result.multi_face_landmarks):
        return False

    face_landmarks = [lm for lm in face_result.multi_face_landmarks[0].landmark]

    for handLms in hands_result.multi_hand_landmarks:
        palm = handLms.landmark[9]  # lokasi tengah telapak

        nose = face_landmarks[1]
        left_eye = face_landmarks[33]
        right_eye = face_landmarks[263]

        # hitung jarak telapak ke wajah
        d1 = euclidean_distance(palm, nose)
        d2 = euclidean_distance(palm, left_eye)
        d3 = euclidean_distance(palm, right_eye)

        # threshold facepalm (agak longgar)
        if d1 < 0.09 or d2 < 0.09 or d3 < 0.09:
            return True

    return False


# ========= Gesture lain =========
def is_fist(landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    closed = 0
    for tip_id in tips_ids[1:]:
        if landmarks[tip_id].y > landmarks[tip_id - 2].y:
            closed += 1
    if landmarks[4].x < landmarks[3].x:
        closed += 1
    return closed == 5


def is_metal(landmarks):
    cond1 = landmarks[8].y < landmarks[6].y
    cond2 = landmarks[20].y < landmarks[18].y
    cond3 = landmarks[12].y > landmarks[10].y
    cond4 = landmarks[16].y > landmarks[14].y
    return cond1 and cond2 and cond3 and cond4


# ========== MAIN CAMERA LOOP ==========
cap = cv2.VideoCapture(0)
prev_y = None
gesture_triggered = None

print("\nGesture yang tersedia:")
print("- Fist up → video1.mp4")
print("- Rock sign → video2.mp4")
print("- FACEPALM → video3.mp4\n")

while True:
    ret, img = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hands_result = hands.process(rgb)
    face_result = face_mesh.process(rgb)

    # ========== DETEKSI FACEPALM ==========
    if is_facepalm(hands_result, face_result):
        if gesture_triggered != 'facepalm':
            print("FACEPALM terdeteksi! Memutar video3.mp4")
            gesture_triggered = 'facepalm'
            play_video("videos/video3.mp4")

    if hands_result.multi_hand_landmarks:
        for handLms in hands_result.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # Fist Up
            if is_fist(handLms.landmark):
                y = handLms.landmark[0].y
                h, w, _ = img.shape
                y_pixel = int(y * h)

                if prev_y is not None:
                    if prev_y - y_pixel > 40 and gesture_triggered != 'fist':
                        print("Fist up terdeteksi! Memutar video1.mp4")
                        gesture_triggered = 'fist'
                        play_video("videos/video1.mp4")
                prev_y = y_pixel

            # Rock Sign
            elif is_metal(handLms.landmark):
                if gesture_triggered != 'metal':
                    print("Gesture metal terdeteksi! Memutar video2.mp4")
                    gesture_triggered = 'metal'
                    play_video("videos/video2.mp4")
                prev_y = None

            else:
                prev_y = None
                gesture_triggered = None

    cv2.imshow("Hand Gesture Recognition + Facepalm", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

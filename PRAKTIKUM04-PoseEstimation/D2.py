import cv2, numpy as np
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("kamera tidak bisa dibuka")

# <--- DIPERBAIKI: 'staticMode'
detector = PoseDetector(staticMode=False, modelComplexity=1, 
                        enableSegmentation=False, detectionCon=0.5, trackCon=0.5)

while True:
    success, img = cap.read()
    if not success:
        print("Gagal membaca frame")
        break

    # <--- DIPERBAIKI: 'findPose'
    img = detector.findPose(img)

    lmList, bboxInfo = detector.findPosition(img, draw=True, bboxWithHands=False)

    # <--- DIPERBAIKI: Semua logika dipindah ke dalam 'if'
    if lmList:
        center = bboxInfo["center"]

        # Gambar lingkaran di tengah bounding box
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED) 
        
        # Cari jarak antara bahu (11) dan pinggul (15) -> ini mungkin salah?
        # Landmark 11 = bahu kiri, 15 = pergelangan tangan kiri
        length, img, info = detector.findDistance(lmList[11][0:2], 
                                                  lmList[15][0:2], 
                                                  img=img, 
                                                  color=(255, 0, 0),
                                                  scale=10)

        # Cari sudut bahu-siku-pergelangan tangan (11, 13, 15)
        angle, img = detector.findAngle(lmList[11][0:2], 
                                        lmList[13][0:2],
                                        lmList[15][0:2],
                                        img=img,
                                        color=(0, 0, 255),
                                        scale=10)
        
        # Cek sudut
        isCloseAngle50 = detector.angleCheck(myAngle=angle, 
                                             targetAngle=50,
                                             offset=10)

        print(isCloseAngle50)

    cv2.imshow("pose + angle ", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# <--- DIPERBAIKI: Indentasi dipindah ke luar loop
cap.release()
cv2.destroyAllWindows()
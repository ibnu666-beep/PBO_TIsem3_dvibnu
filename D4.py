import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("kamera tidak bisa dibuka")

detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

while True:
    ok, img = cap.read()
    if not ok: 
        break
        
    hands, img = detector.findHands(img, draw=True, flipType=True)
    
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        count = sum(fingers)
        
        cv2.putText(img, f"fingers: {count} {fingers}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    cv2.imshow("hands + fingers", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
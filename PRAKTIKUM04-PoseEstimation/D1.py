import cv2, time

cap = cv2.VideoCapture(0)
if not cap.isOpened():
  raise RuntimeError("kamera tidak bisa dibuka. coba index 1/2.")

frames, t0 = 0, time.time()
while True:
  ok, frame = cap.read()
  if not ok: break
  frames += 1
  if time.time() - t0 >= 1.0:
    cv2.setWindowTitle("preview", f"preview (FPS ~ {frames})") 
    frames, t0 = 0, time.time()
  cv2.imshow("preview", frame)
  if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
import cv2

cam_index = 1

cap = cv2.VideoCapture(cam_index, cv2.CAP_AVFOUNDATION)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5) 
cap.set(cv2.CAP_PROP_CONTRAST, 0.5)  
cap.set(cv2.CAP_PROP_EXPOSURE, -4)  

if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break
    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import time
import math as math
from pythonosc.udp_client import SimpleUDPClient
import json

UDP_IP = "127.0.0.1"  
UDP_PORT = 8000

COLOR_DIST = (255, 122, 178)
COLOR_SKELETON = (255, 255, 255)
COLOR_ROOT = (255, 0, 90)
COLOR_FINGERS = (255, 122, 178)
COLOR_CENTROID = (255, 0, 90)
COLOR_DIST_HANDS = (255, 255, 255)

class HandTrackingDynamic:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.__mode__   =  mode
        self.__maxHands__   =  maxHands
        self.__detectionCon__   =   detectionCon
        self.__trackCon__   =   trackCon
        self.handsMp = mp.solutions.hands
        self.hands = self.handsMp.Hands()
        self.mpDraw= mp.solutions.drawing_utils
        self.landmark_spec = self.mpDraw.DrawingSpec(COLOR_SKELETON, thickness=1, circle_radius=1)
        self.connection_spec = self.mpDraw.DrawingSpec(COLOR_SKELETON, thickness=1, circle_radius=1)
        self.tipIds = [4, 8, 12, 16, 20]
        self.lmsList = [[], []]
        self.params = {
            'p1': None, # dist between thumb and index
            'p2': None, # dist between thumb and middle
            'p3': None, # dist between thumb and ring
            'p4': None, # dist between thumb and pinky
            'p5': None, # pinch 
            'p6': None, # same as above, for second hand in frame
            'p7': None,
            'p8': None,
            'p9': None, 
            'p10': None,
            'p11': None, # dist between hands 
        }
        self.last_params = {
            'p1': [None, 50], 
            'p2': [None, 50],
            'p3': [None, 50],
            'p4': [None, 50],
            'p5': [None, 50],
            'p6': [None, 50],
            'p7': [None, 50],
            'p8': [None, 50],
            'p9': [None, 50],
            'p10': [None, 50],
            'p11': [None, 50],
        }

    def findFingers(self, frame, draw=True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape  
        self.results = self.hands.process(imgRGB)  
        if self.results.multi_hand_landmarks: 
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.handsMp.HAND_CONNECTIONS, self.connection_spec, self.landmark_spec)
        return frame

    def findPosition(self, frame, handNo=0, draw=True):
        if self.results.multi_hand_landmarks:
            h, w, _ = frame.shape
            for handNo, hand in enumerate(self.results.multi_hand_landmarks):
                xList =[]
                yList =[]
                for lmk_id, lm in enumerate(hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    xList.append(cx)
                    yList.append(cy)
                    if len(self.lmsList) > handNo:
                        self.lmsList[handNo].append([lmk_id, cx, cy])
        return frame
        
    def calculateParams(self, frame):

        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) == 1:
                hand = self.results.multi_hand_landmarks[0]
                self.params['p1'] = self.findFingerDistance(hand.landmark[4], hand.landmark[8], frame, draw=True)
                self.params['p2'] = self.findFingerDistance(hand.landmark[4], hand.landmark[12], frame, draw=True)
                self.params['p3'] = self.findFingerDistance(hand.landmark[4], hand.landmark[16], frame, draw=True)
                self.params['p4'] = self.findFingerDistance(hand.landmark[4], hand.landmark[20], frame, draw=True)
                self.params['p5'] = self.findPinch(frame, hand)
                self.params['p6'] = None
                self.params['p7'] = None
                self.params['p8'] = None
                self.params['p9'] = None
                self.params['p10'] = None
                self.params['p11'] = None
            elif len(self.results.multi_hand_landmarks) == 2: # 2nd hand in frame
                hand1 = self.results.multi_hand_landmarks[0]
                self.params['p1'] = self.findFingerDistance(hand1.landmark[4], hand1.landmark[8], frame, draw=True)
                self.params['p2'] = self.findFingerDistance(hand1.landmark[4], hand1.landmark[12], frame, draw=True)
                self.params['p3'] = self.findFingerDistance(hand1.landmark[4], hand1.landmark[16], frame, draw=True)
                self.params['p4'] = self.findFingerDistance(hand1.landmark[4], hand1.landmark[20], frame, draw=True)
                self.params['p5'] = self.findPinch(frame, hand1)
                hand2 = self.results.multi_hand_landmarks[1]
                self.params['p6'] = self.findFingerDistance(hand2.landmark[4], hand2.landmark[8], frame, draw=True)
                self.params['p7'] = self.findFingerDistance(hand2.landmark[4], hand2.landmark[12], frame, draw=True)
                self.params['p8'] = self.findFingerDistance(hand2.landmark[4], hand2.landmark[16], frame, draw=True)
                self.params['p9'] = self.findFingerDistance(hand2.landmark[4], hand2.landmark[20], frame, draw=True)
                self.params['p10'] = self.findPinch(frame, hand2)
                self.params['p11'] = self.findHandDistance(frame, hand1, hand2)
        else:
            self.params['p1'] = None
            self.params['p2'] = None
            self.params['p3'] = None
            self.params['p4'] = None
            self.params['p5'] = None
            self.params['p6'] = None
            self.params['p7'] = None
            self.params['p8'] = None
            self.params['p9'] = None
            self.params['p10'] = None
            self.params['p11'] = None
        
        # print(self.params) # DEBUG
        return frame
    
    def findFingerDistance(self, p1, p2, frame, draw=True, r=10, t=3):
        h, w, _ = frame.shape
        x1, y1 = int(p1.x * w), int(p1.y * h)
        x2, y2 = int(p2.x * w), int(p2.y * h)
        if draw:
              cv2.line(frame, (x1, y1),(x2, y2), COLOR_DIST, t)
              cv2.circle(frame, (x1, y1), r, COLOR_FINGERS, cv2.FILLED)
              cv2.circle(frame, (x2, y2), r, COLOR_FINGERS, cv2.FILLED)
        distance = math.hypot(x2-x1, y2-y1)
        return distance    
    
    def findPinch(self, frame, hand): # get average distance between fingers and thumb
        h, w, _ = frame.shape
        x0 = hand.landmark[4].x * w
        y0 = hand.landmark[4].y * h
        distance = 0
        for i in [8, 12, 16, 20]:
            x = hand.landmark[i].x * w
            y = hand.landmark[i].y * h
            distance = distance + math.hypot((x0-x), (y0-y))
        distance = distance / 4   
        return distance

    def findHandDistance(self, frame, hand1, hand2, draw=True, r=10, t=1):
        h, w, _ = frame.shape
        c = [[],[]] # centroids
        for i, hand in enumerate((hand1, hand2)):    
            cx = 0
            cy = 0
            for lmk in hand.landmark:
                cx = cx + int(lmk.x * w)
                cy = cy + int(lmk.y * h)
            cx = cx // len(hand.landmark)
            cy = cy // len(hand.landmark)
            c[i] = [cx, cy]
            if draw:
                cv2.circle(frame, (cx, cy), r, COLOR_CENTROID, cv2.FILLED)
        distance = math.hypot(c[0][0] - c[1][0], c[0][1] - c[1][1])
        if draw:
            cv2.line(frame, (c[0][0], c[0][1]), (c[1][0], c[1][1]), COLOR_DIST_HANDS, t)
        return distance

    def sendOSC(self, client, msg):
        for p, val in self.params.items():
            if val and self.last_params[p][1] > 3:
                if val < 50:
                    if self.last_params[p][0]:
                        if abs(val - self.last_params[p][0]) > 20:
                            client.send_message(msg, str(p))
                            self.last_params[p][1] = 0
                    else:
                        client.send_message(msg, str(p))    
                        self.last_params[p][1] = 0
            self.last_params[p] = [self.params[p], self.last_params[p][1] + 1]

        # data_json = json.dumps(data)
        # client.send_message(msg, data_json)
                    
if __name__ == "__main__":

    cam_index = 1
    ctime = 0 
    ptime = 0 
    scale_factor_in = 0.5
    scale_factor_out = 0.7
    cap = cv2.VideoCapture(cam_index, cv2.CAP_AVFOUNDATION)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    window_name = f'Camera {cam_index}'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    print(f"[INFO] Initiated camera capture ({width}x{height})")

    detector = HandTrackingDynamic()
    client = SimpleUDPClient(UDP_IP, UDP_PORT)

    if not cap.isOpened():
        print("[ERROR] Cannot open camera")
        exit()

    try: 
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Failed to capture frame from camera.")
                break
            
            frame = cv2.resize(frame, None, fx=scale_factor_in, fy=scale_factor_in, interpolation=cv2.INTER_LINEAR)
            frame = cv2.flip(frame, 1)
            frame = detector.findFingers(frame)
            frame = detector.findPosition(frame)
            detector.calculateParams(frame)
            detector.sendOSC(client, '/params')

            ctime = time.time()
            fps = 1 / (ctime - ptime)
            ptime = ctime

            cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

            output_frame = cv2.resize(frame, (round(width*scale_factor_out), round(height*scale_factor_out)), interpolation=cv2.INTER_LINEAR)
            cv2.resizeWindow(window_name, round(width*scale_factor_out), round(height*scale_factor_out))
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print(" Exiting...")

    cap.release()
    cv2.destroyAllWindows()
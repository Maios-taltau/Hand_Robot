import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
#เตรียมข้อมูลสำหรับตวจจับภาพ
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

h = 480
w = 640

# Use CV2 Functionality to create a Video stream and add some values + variables
cap = cv2.VideoCapture(0)
tip = [8, 12, 16, 20]
tipname = [8, 12, 16, 20]
fingers = []
finger = []
def findpostion(frame1):
    list=[]
    #แปลงค่าสีเพราะ เราต้องทำงานโดนใช้ RGB แต่ ค่าสีที่ได้จาก webcam เป็นแบบ BRG
    frame2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    #สร้าง object ที่เรัยค่าสี RGB เพื่อมาเก็บค่าต่างๆของผลลัพธ์
    results = hands.process(frame2)

    if results.multi_hand_landmarks:
       for handLandmarks in results.multi_hand_landmarks:
           #วาดเส้รแสดงจุดต่างๆ 21 จุด
           mp_drawing.draw_landmarks(frame1, handLandmarks, mp_hands.HAND_CONNECTIONS)
           list=[]
           for id, pt in enumerate (handLandmarks.landmark):
                ##ค่าที่มาจาก handLandmarks จะเป็น % ของขนาดภาพ โดย x จะเทียบกับความกว้าง และ y จะเทียบกับความสูง
                x = int(pt.x * w)
                y = int(pt.y * h)
                list.append([id, x, y])
    return list

def findnameoflandmark(frame1):
     list=[]
     frame2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
     results = hands.process(frame2)
     if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            #ค่าที่ได้ออกมาเป็นชื่อของตำแหน่งทั้ง 21 ตำแหน่ง
            for point in mp_hands.HandLandmark:
                 list.append(str(point).replace ("< ", "").replace("HandLandmark.", "").replace("_", " ").replace("[]", ""))
     return list

# Create an infinite loop which will produce the live feed to our desktop and that will search for hands
while True:
    #Thumb => นิ้วหัวแม่มือ, Index => นิ้วชี้, Middle => นิ้วกลาง, Ring => นิ้วนาง, Pinky => นิ้วก้อน
    ret, frame = cap.read()
    frame1 = cv2.resize(frame, (640, 480))
    a = findpostion(frame1)
    b = findnameoflandmark(frame1)
    if len(b and a) != 0:
        finger = []
        #เช็ค Thumb
        if a[0][1:] < a[4][1:]:
            finger.append(1)
            print(b[4])
        else:
            finger.append(0)
            print('No Thumb')
        fingers = []
        #เช็ค Index Middle Ring Pinky
        for id in range(0, 4):
            if a[tip[id]][2:] < a[tip[id] - 2][2:]:
                print(b[tipname[id]])

                fingers.append(1)
            else:
                fingers.append(0)
                print('No ' + b[tipname[id]])
        print('-'*30)
    frame1 = cv2.flip(frame1, 1)
    cv2.imshow("Frame", frame1)
    key = cv2.waitKey(1) & 0xFF
    # Below states that if the |s| is press on the keyboard it will stop the system
    if key == 27:
        break
from flask import Flask, render_template, Response
import cv2

cap = cv2.VideoCapture(0)
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('Webcam_server.html')
def genFrames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray,1.1,4)
            for (x,y,w,h) in faces:
               cv2.rectangle(frame,(x,y),(x+w, y+h),(255,255,0),2)
               roi_gray = gray[y:y+h,x:x+w]
               roi_color = frame[y:y+h,x:x+w]
               
            ret, buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/Streaming')
def Streaming():
    return Response(genFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
   app.run()

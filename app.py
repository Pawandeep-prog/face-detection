from flask import Flask, Response, render_template, request
import cv2

# cv2 for video related function

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(get(), mimetype='multipart/x-mixed-replace; boundary=frame')

def get():
    cap = cv2.VideoCapture(0)

    cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while True:
        _, frm = cap.read()

        gfrm = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

        cords = cascade.detectMultiScale(gfrm, 1.1, 3)

        for x,y,w,h in cords:  
            cv2.rectangle(frm, (x,y), (x+w, y+h), (0,255,0), 3)

        frm = cv2.imencode('.jpg', frm)[1].tobytes()

        try:
            data = request.args.get('btn')

            if data=='stop':
                cap.release()

        except:
            pass

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frm + b'\r\n')


@app.route('/stop')
def stop():
    return render_template('bye.html')

if __name__ == "__main__":
    app.run(debug=True)


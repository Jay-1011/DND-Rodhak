from flask import Flask, render_template, Response

from camera_pi import Camera
import pyrebase

app = Flask(__name__)

# Initialize Firebase
firebase_config = {
                    "apiKey": "AIzaSyCtEfqT5d9arMVa-bVj1s60-oGnLpJjtMQ",
                    "authDomain": "dashboard-45d5b.firebaseapp.com",
                    "databaseURL": "https://dashboard-45d5b-default-rtdb.firebaseio.com",
                    "projectId": "dashboard-45d5b",
                    "storageBucket": "dashboard-45d5b.appspot.com",
                    "messagingSenderId": "350541968825",
                    "appId": "1:350541968825:web:502c78f71f55f7d403f268",
                    "measurementId": "G-15Y4TSWLJ5"
                    }
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()


@app.route('/update/<value>')
def update_value(value):
    """Updating value."""
    db.child('Value 8').update({'Mhye8whdoiwnd': value})
    return render_template('index.html', value_8=value)


@app.route('/')
def index():
    """Video streaming home page."""
    values = db.child('Value 8').get()
    for value in values.each():
        value = value.val()
    return render_template('index.html', value_8=value)


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

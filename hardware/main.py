from flask import Flask, Response
from camera import FaceRecognitionCCTV
from buzzer import BuzzerControl
from led import LEDControl


### Flask app to send video stream to server/webpage 
### and control GPIO pins via REST api

# flask app
app = Flask(__name__)

class IOUtil(object):
    def __init__(self):
        self.buzzer = BuzzerControl()
        self.led = LEDControl()
    
    def change_led(self, operation):
        if operation == 0:
            self.led.turn_off()
            return 1
        
        elif operation == 1:
            self.led.turn_on()
            return 1
        else:
            print('operation does not exist')
            return 0
    
    def change_buzzer(self, operation):
        if operation == 0:
            self.buzzer.turn_off()
            return 1
        
        elif operation == 1:
            self.buzzer.turn_on()
            return 1
        else:
            print('operation does not exist')
            return 0
    


# generate video feed with face recognition
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# api to return video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen(FaceRecognitionCCTV()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# api to set LED
# operation: 0 for turn off, 1 for turn on
@app.route('/led/<int:operation>')
def led(operation):
   if operation==0:
       io_util.change_led(operation)
       return 'led turned on'
   elif operation==1:
       io_util.change_led(operation)
       return 'led turned off'
   else:
       return 'invalid led operation'

# api to set buzzer
# operation: 0 for turn off, 1 for turn on
@app.route('/buzzer/<int:operation>')
def buzzer(operation):
   if operation==0:
       io_util.change_buzzer(operation)
       return 'buzzer turned on'
   elif operation==1:
       io_util.change_buzzer(operation)
       return 'buzzer turned off'
   else:
       return 'invalid buzzer operation'

# initiate IOUtil instance
io_util = IOUtil()

if __name__ == '__main__':
    app.run(debug=True)
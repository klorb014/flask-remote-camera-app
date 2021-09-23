from flask import Flask, render_template, Response, request
import logging
from camera_controller import CameraController
from camera import Resolution


app = Flask(__name__)
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
controller = CameraController()
controller.find_available_cameras()


@app.route('/video_feed', methods = ['GET'])
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    if request.method == 'GET':
        logging.info(request.args)
        if len(request.args) != 0:
            device_name = request.args['camera']
            logging.info(device_name)
            return Response(controller.open_feed(device_name), mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            device_name = "camera-0"
            controller.switch_cameras(device_name)
            return Response(controller.open_feed(device_name), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/switch_feed', methods = ['GET'])
def switch_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    if request.method == 'GET':
        logging.info(request.args)
        if len(request.args) != 0:
            device_name = request.args['camera']
            logging.info(device_name)
            if controller.switch_cameras(device_name, Resolution.LOW, True):
                return Response("{'switch':'true'}", status=200, mimetype='application/json')
        else:
            controller.close_all_feeds()
            device_name = "camera-0"
            if controller.switch_cameras(device_name):
                return Response("{'switch':'true'}", status=200, mimetype='application/json')

    return Response("{'switch':'false'}", status=400, mimetype='application/json')


@app.route('/')
def index():
    """Video streaming home page."""
    cameras=controller.available_cameras.keys()
    return render_template('index.html', camera_list=cameras)


if __name__ == '__main__':
    app.run(debug=True)
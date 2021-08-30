import json
from re import DEBUG, sub
import subprocess
import os
import cv2
import Cam_Handgesture
from werkzeug.utils import secure_filename, send_from_directory
from flask import Flask, render_template, request,Response, redirect, send_file, url_for

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
# print(app.instance_path, uploads_dir)
os.makedirs(uploads_dir, exist_ok=True)
frame =  cv2.imread('static/image-5.jpg')
# frame = cv2.imread("static/load_loading.gif")
JSON_FLAG_FILE = 'static/flag.json'
# cap = cv2.VideoCapture(0)
@app.route("/")
def hello_world():

    return render_template('index.html')

def generate_video():
    while True:
        global frame
        frame = Cam_Handgesture.PassImages()
        # success, frame = cap.read()


        # cv2.imshow("mywinn", newImg)
        # cv2.waitKey(1)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes+ b'\r\n')


@app.route("/CameraAction", methods=['POST'])
def CameraAction():
    process_status = "Unknown"
    try:
        if not request.method == "POST":
            return process_status
        print(request.get_data().decode('UTF-8'))
        if request.get_data().decode('UTF-8') == "StartCamera":
            process_status = Cam_Handgesture.OpenCam_StartGesture_Recog(openCam_command=True)
            return process_status
        elif request.get_data().decode('UTF-8') == "StopCamera":
            process_status = Cam_Handgesture.OpenCam_StartGesture_Recog(openCam_command=False)
            global frame
            frame = cv2.imread('static/image-5.jpg')
            return process_status
    except:
        process_status = "Process Stopped"
    return process_status
#
# @app.route("/detect", methods=['POST'])
# def detect():
#     with open(JSON_FLAG_FILE, "r") as jsonFile:
#         Flag_data = json.load(jsonFile)
#
#     Flag_data["flag"] = "RUN"
#
#     with open(JSON_FLAG_FILE, "w") as jsonFile:
#         json.dump(Flag_data, jsonFile)
#     global frame
#     # frame = cv2.imread("static/eqw.png")
#     if not request.method == "POST":
#         return
#     print(request.form.get("InputType"))
#     if request.form.get("InputType") == "Inputfile":
#         video = request.files['Video']
#         print(video)
#         video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
#         Video_File_Path = "instance/uploads/"+secure_filename(video.filename)
#         print(secure_filename(video.filename))
#         global frame
#         frame = Run_Obj_Detect(Video_File_Path)
#     elif request.form.get("InputType") == "URL":
#         print(request.form.get("Video"))
#         src_url = request.form.get("Video")
#
#         frame = Run_Obj_Detect(src_url)

    # cv2.imshow("Mywin", frame)
    # cv2.waitKey(0)
    # subprocess.run("ls")
    # subprocess.run(['python3', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename))])

    # return os.path.join(uploads_dir, secure_filename(video.filename))
    # obj = secure_filename(video.filename)
    # return "Your response was recieved"


@app.route('/video', methods=['GET'])
def video():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')



# @app.route('/Stopprocess', methods=['POST'])
# def Stopprocess():
#     with open(JSON_FLAG_FILE, "r") as jsonFile:
#         Flag_data = json.load(jsonFile)
#
#     Flag_data["flag"] = "KILL"
#
#     with open(JSON_FLAG_FILE, "w") as jsonFile:
#         json.dump(Flag_data, jsonFile)
#
#     global frame
#     frame = cv2.imread('static/Loader.jpg')
#
#     return Flag_data
# @app.route('/return-files', methods=['GET'])
# def return_file():
#     obj = request.args.get('obj')
#     loc = os.path.join("runs/detect", obj)
#     print(loc)
#     try:
#         return send_file(os.path.join("runs/detect", obj), attachment_filename=obj)
#         # return send_from_directory(loc, obj)
#     except Exception as e:
#         return str(e)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
    # serve(app)

    # with open(JSON_FLAG_FILE, "r") as jsonFile:
    #     Flag_data = json.load(jsonFile)
    #
    # Flag_data["flag"] = "RUN"
    #
    # with open(JSON_FLAG_FILE, "w") as jsonFile:
    #     json.dump(Flag_data, jsonFile)



# @app.route('/display/<filename>')
# def display_video(filename):
# 	#print('display_video filename: ' + filename)
# 	return redirect(url_for('static/video_1.mp4', code=200))

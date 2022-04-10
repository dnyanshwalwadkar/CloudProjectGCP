from flask import Response, jsonify
from flask import Flask, render_template,request
from flask_cors import CORS
import json
from getNumberPlateVals import detect_license_plate
import base64
import os
from db import get_users, add_users, deleteUser, updateUser
# from predict_iages import DetectVehicleNumberPlate
from predict_images import DetectVehicleNumberPlate


from flask import Flask, render_template, url_for, flash, redirect, request
import os







application = Flask(__name__)
PASSWORD = "root"
PUBLIC_IP_ADDRESS = "81.149.206.233"
DBNAME = "userdata"
PROJECT_ID = "cloudproject-345422"
INSTANCE_NAME = "numberplate"

# configuration


os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
CORS(application)

inputFileName = "inputImage.jpg"
imagePath = "images/" + inputFileName
image_display = True
pred_stagesArgVal = 2
croppedImagepath = "images/croppedImage.jpg"


class ClientApp:
    def __init__(self):
        # modelArg = "datasets/experiment_faster_rcnn/2018_08_02/exported_model/frozen_inference_graph.pb"
        self.modelArg = "datasets/experiment_ssd/2018_07_25_14-00/exported_model/frozen_inference_graph.pb"
        self.labelsArg = "datasets/records/classes.pbtxt"
        self.num_classesArg = 37
        self.min_confidenceArg = 0.5
        filepath = "autoPartsMapping/partNumbers.xlsx"
        # self.regPartDetailsObj = ReadPartDetails(filepath)
        self.numberPlateObj = DetectVehicleNumberPlate()


def decodeImageIntoBase64(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    try:
        with open(croppedImagePath, "rb") as f:
            return base64.b64encode(f.read())
    except:

        return base64.b64encode(croppedImagePath)

# @application.route('/html')
# def static_page():
#      return render_template('Home.html')




@application.route('/user', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        add_users(request.get_json())
        return 'User Added'

    return get_users()

@application.route('/user/delete', methods=['DELETE'])
def usersDelete():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        deleteUser(request.get_json())
        return 'User Deleted'

@application.route('/user/update', methods=['POST'])
def usersUpdate():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        updateUser(request.get_json())
        return 'User Updated'



@application.route("/predict", methods=["POST"])
def getPrediction():

    #inpImage = request.form.values()
    inpImage = request.json['image']
    imagePath = "images/" + inputFileName
    decodeImageIntoBase64(inpImage, imagePath)

    #inpImage = encodeImageIntoBase64(bytes(inpImage))
    #inpImage = request.json['image']
    #decodeImageIntoBase64(inpImage, imagePath)
    # responseList = []
    # it's a temporary variable just for testing
    # imagePath = "images/car.jpg"
    try:
        labelledImage = clApp.numberPlateObj.predictImages(imagePath, pred_stagesArgVal,
                                                           croppedImagepath, clApp.numberPlateObj)
        if labelledImage is not None:
            encodedCroppedImageStr = encodeImageIntoBase64(croppedImagepath)
            ig = str(encodedCroppedImageStr)
            ik = ig.replace('b\'', '')
            numberPlateVal = detect_license_plate(ik)
            if len(numberPlateVal) == 10:
                # returnedVal = clApp.regPartDetailsObj.getNumberDetails(numberPlateVal)
                # responseDict = {"base64Image": ik, "partDetails" : returnedVal, "numberPlateVal": numberPlateVal}
                responseDict = {"base64Image": ik, "numberPlateVal": numberPlateVal}
                # responseList.append(responseDict)
                # print(responseDict)
                # convert to json data
                jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
                #print(jsonStr.decode())
                return Response(jsonStr.decode())
            else:
                # responseDict = {"base64Image": "Unknown", "partDetails" : "Unknown", "numberPlateVal": "Unknown"}
                responseDict = {"base64Image": "Unknown", "numberPlateVal": "Unknown"}
                # responseList.append(responseDict)
                # print(responseDict)
                # convert to json data
                print("hello-else-2")
                jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
                # print(jsonStr.decode())
                return Response(jsonStr.decode())
        else:
            # responseDict = {"base64Image": "Unknown", "partDetails" : "Unknown", "numberPlateVal": "Unknown"}
            responseDict = {"base64Image": "Unknown", "numberPlateVal": "Unknown"}
            # responseList.append(responseDict)
            # print(responseDict)
            # convert to json data
            print("hello-else-1")
            jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
            # print(jsonStr.decode())
            print("hello-else")
            return Response(jsonStr.decode())
    except Exception as e:
        print("hello",e)
    # responseDict = {"base64Image": "Unknown", "partDetails": "Unknown", "numberPlateVal": "Unknown"}
    responseDict = {"base64Image": "Unknown", "numberPlateVal": "Unknown"}
    # responseList.append(responseDict)
    # print(responseDict)
    # convert to json data
    jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
    # print(jsonStr.decode())
    return Response(jsonStr.decode())
    #return render_template('Home.html',prediction_text="hello how are you" )
    # return Response("Invalid Input")


# port = int(os.getenv("PORT"))
if __name__ == '__main__':
    clApp = ClientApp()
    # # host = "127.0.0.1"
    # host = '127.0.0.1'
    # port = 5000
    #httpd = simple_server.make_server(host, port, application)
    # print("Serving on %s %d" % (host, port))
    #httpd.serve_forever()
    application.run()

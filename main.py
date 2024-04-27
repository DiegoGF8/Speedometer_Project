import cv2
import os
import sys
import signal
import time
import board
import busio
from periphery import I2C
from edge_impulse_linux.image import ImageImpulseRunner

import preba

# initialize variables for Edge Impulse
runner = None
dir_path = os.path.dirname(os.path.realpath(__file__))#The father path of the actual path --- /home/jp/Desktop
modelfile = os.path.join(dir_path, "modelfile.eim")#The father path with the actual path and, with the"model.eim" --- /home/jp/Desktop/modelFILE.eim
print(dir_path)
print(modelfile)

#Defining some functions to use in the future
def now():
    return round(time.time() * 1000)

def sigint_handler(sig, frame):
    print('Interrupted')
    if (runner):
        runner.stop()
    sys.exit(0)

def verify_ML(runner, videoCaptureDeviceId):
    for res, img in runner.classifier(videoCaptureDeviceId):
        if (next_frame > now()):
            time.sleep((next_frame - now()) / 1000)

        if "classification" in res["result"].keys():
            #print('Result (%d ms.) ' % (
                #res['timing']['dsp'] + res['timing']['classification']), end='')
            for label in labels:
                score = res['result']['classification'][label]
                #print('%s: %.2f\t' % (label, score), end='')
            print('', flush=True)            
        
        elif "bounding_boxes" in res["result"].keys():
            print('Found %d bounding boxes (%d ms.)' % (len(
                res["result"]["bounding_boxes"]), res['timing']['dsp'] + res['timing']['classification']))

            for bb in res["result"]["bounding_boxes"]:
                #print('\t%s (%.2f): x=%d y=%d w=%d h=%d' % (bb['label'], bb['value'], bb['x'], bb['y'], bb['width'], bb['height']))
                vehicle_type = bb["label"]
                confidence = round(bb["value"] * 100)
                print("what is it? " + vehicle_type +
                    " and how confident? " + str(confidence))




signal.signal(signal.SIGINT, sigint_handler)

#Where we start the AI process with Edge Impulse
def main():
 with ImageImpulseRunner(modelfile) as runner:
	 #SETUP:
        try:
            model_info = runner.init()
            print('Loaded runner for "' +
                  model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')
            labels = model_info['model_parameters']['labels']

            videoCaptureDeviceId = 0

            camera = cv2.VideoCapture(videoCaptureDeviceId)
            ret = camera.read()[0]
            
            if ret:
                backendName = camera.getBackendName()
                w = camera.get(3)
                h = camera.get(4)
                print("Camera %s (%s x %s) in port %s selected." %
                      (backendName, h, w, videoCaptureDeviceId))
                camera.release()
            else:
                raise Exception("Couldn't initialize selected camera.")
 
            next_frame = 3  # limit to ~10 fps here
                                    
                    # get the speed of the object before we start any processing                    
            current_speed = preba.ops_get_speed()
            verify_ML(runner, videoCaptureDeviceId)
                    

            next_frame = now() + 100
        finally:
            if runner:
                runner.stop()

while True:
    main()

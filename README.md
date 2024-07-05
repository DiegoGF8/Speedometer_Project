# Speedometer_Project

This project aims to register the speed of a vehicle and recognize the type of vehicle. The goal is to create a ticket camera for a city, providing a more affordable solution for the city in question. The implementation of this project involves using multiple components. The first component to be used is a Raspberry Pi, a camera compatible with the Raspberry Pi, and an Omnipresence OPS243-A Doppler Radar Sensor. For the software, you will need to use Python version 3.12.3, Arduino IDE, and a machine learning application named EdgeImpulse.

For initiating this project, you will need both the Doppler sensor and a Raspberry Pi. You will connect and configure both of these, and you will be able to verify if this is done correctly by checking the serial communication (COM). For this, you can use the Arduino IDE program, which allows you to easily check by opening a window where you can see in real time the information that the sensor receives from the objects in front. This information includes the distance and the speed of the object in front of it.

For configuring the sensor in the Raspberry Pi, the next step is to create a Python object detection library using the Edge Impulse online tool. In this tool, you will first need to go to the main menu and then create a new project. You will need to select the object detection section of the tool. In this section, you will need to take pictures, as recommended, or you can download them from the internet to let the machine learning tool train in object detection.

The steps in the tool for generating a machine learning library for object detection are:

1. Add data by providing new data. We upload 156 images of cars; these were pictures that we took of cars on the street.
2. When the system is collecting the data, you will need to verify the object detection on the images. This is done by adding a label, in this case, with the name "car," and then you will verify that the tool recognizes the items or if you need to add the label to each image.  
3. Then you will start creating a pulse
4. After starting to create a pulse, you will need to provide the image specifications and the data specifications in the object detection part. In this part, we use 156 images of cars.
5. After this, you will be done with the specifications of the program, and finally, you select the option to start training.

After the training is completely done, you will be able to see a percentage of accuracy that the system has for object detection, as well as the percentage of failure in object detection and the reaction time per item. This information will appear for each label that you have created in the pulse. The only characteristic that these labels share is the reaction time frame that the system has to respond and the RAM used.

Now you have to install Edge Impulse on Linux. The following steps are only for Raspberry Pi 4, and this is a list of commands that you will need to follow. The first command that you will need to apply is the following:
```
curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -
sudo apt install -y gcc g++ make build-essential nodejs sox gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps
npm config set user root && sudo npm install edge-impulse-linux -g --unsafe-perm
```

Then you will need to get installed the edge implse linux python SDK 
```
sudo apt-get install libatlas-base-dev libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
pip3 install edge_impulse_linux -i https://pypi.python.org/simple
```

By doing this, you will finally apply: 
```
edge-impulse-linux-runner --download model.eim
```

After this installation, the python code will need to make the (machine learning) ML model to identify a vehicule, measure the speed of the vehicule and show it into a window to know the specification of this. 

For this part, the following code will display the the data collected by the OPS sensor:
```
import serial

#Establece la comunicacion serial con el puerto ACM0 a un baudrate de 9600
ser = serial.Serial(port="/dev/ttyACM0",baudrate=9600)

def send_serial_cmd(print_prefix, command):
    """
    function for sending serial commands to the OPS module
    """
    data_for_send_str = command
    data_for_send_bytes = str.encode(data_for_send_str)
    print(print_prefix, command)
    ser.write(data_for_send_bytes)
    # initialize message verify checking
    ser_message_start = '{'
    ser_write_verify = False
    # print out module response to command string
    while not ser_write_verify:
        data_rx_bytes = ser.readline()
        data_rx_length = len(data_rx_bytes)
        if data_rx_length != 0:
            data_rx_str = str(data_rx_bytes)
            if data_rx_str.find(ser_message_start):
                ser_write_verify = True

# Las constantes que tiene el modulo
Ops_Speed_Output_Units = ['US', 'UK', 'UM', 'UC']#US = mph,   UK=KMPH!!,     UM=mps,UC= Cmps

# Colocarle al sensor los valores que deseamos ver
send_serial_cmd("\nSet Speed Output Units: ", Ops_Speed_Output_Units[1])

#Lee en UTF-8 los bits que recibe el puerto y ajusta los datos para que salgan ordenados en la terminal.
def ops_get_speed():
    while True:
        Ops_rx_bytes = ser.readline()        
        try:
            data = Ops_rx_bytes.decode("utf-8").replace("\r\n","").replace("\"","")#Limpia la linea obtenida, le quita cosas.
            data = data.split(",")#Separa los valores obtenidos, la unidad y el valor, en vez de estar junto.
            if "kmph" in data[0]:
                #print("Unit: ",data[0])
                print(float(data[1]), "Kmph")
            else:
                print("No speed detected")
        except Exception as error:
            print(error)

ops_get_speed()
```

This code, will show the information about on the the format in which we want the data to be displayed.

When you have already all the information installed, then we have to pass to the part of connecting a camera to the raspberry pi, on our case we use a web-cam that connects via usb-a, for the case of the raspberry pi 4 you will need to have a camera that conects on usb 3.0 for this to work correct. 

After using this program, the next step is to connect the camera, the ML obect detection model and the Doppler sensor for being able to capture the image of the camera when this detects an vehicule if this pass the maximun speed stablished, so this code will be able to generate a document when the image is saved with the data of the object that was detected by the camera. 
```
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
```
By the way, the project is still in progress, so it is not complete as of this date, 04-26-2024. However, all the data and documentation about this are available in this repository created by Juan Pablo Zebadúa Engel and Diego José Girón Figueroa.

We based our project on the following projects from the web:
```
https://www.hackster.io/rob-lauer/busted-create-an-ml-powered-speed-trap-b1e5d1
```
```
https://github.com/rdlauer/pispeedtrap
```


   

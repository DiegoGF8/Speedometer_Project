# Speedometer_Project

This project is looking for being able to register the speed of a vehicle and be able to recognize the type of vehicle. This is looking to become a ticket camera for a city, so this will be a more afordable way to provide this to the city in cuestion. The implementation of this project is done by using multiple elemente. The first that will be use is a raspberry pi, a camera compatible with the raspberry and also an omnipresence OPS243-A Doppler Radar Sensor; for the software you wil need to use python version 3.12.3, arduino ID and also the use of a machine learning app name EdgeImpulse. 

For initiating this project, you will need to have both the Dopller sensor and a raspberry pi. You will conect and configure both of this and you will be able to notice if this is done correctly by verifying the serial communication (COM) and for this you can use the arduino IDE program as this let you check in a easy way as this program let you open a window where you can see in real time the information that the sensor is able to receive form the objects in front, this will be the distance and the speed of the object in front of this. 
```
hola
```

Afer being the configuration of the sensor in the raspberry pi, the next step is to creat a python object detection library by using the tool of edge impulse online. Into this tool you first will need to go into the main menu and after this you will creat a new project. This will need you to select the object detection section on the tool. Into this you will need to take pictures as a recommendation or you can download this fomr the internet for letting the machine learning tool train in the object detection. 

The steps into the tool for generating a machine learning library of object detection are: 

1. add datsa by providing new data, we upload the quantity of 156 images of cars, this were ictures that we take of cars on the street.
2. when the  system is collecting the data, you will need to verify the object detection on the images, this will be done by adding a label in this case with the name of car, ande then you will berify that the tool recognizes the items or if you will need to add the label on each image.   
3. then you will start creating a pulse
4. after starting creating a pulse, you will need to oprovide the image specificaitons, and the data specifications into the object detection part, in this part we use the ammount of 156 iages of cars.
5. after this you will be done with the speccifications of the program, and finally you select the option of start training.
   After the training is completely done, you will be able to watch a porcentage of accuary that the system has for the object detection, also the porcentage of failure on objet detection and the time reaction by    item. This information will appear for each label that you have created on the pulse, the only caracteristic that this labels share are the time reaction timeframe that the system has to response and the RAM       used.

Now you have to install the Ede impulse on linux, the following states are only for raspberry pi 4 and this is a list of commands that you will need to follow. 
the rfisrt command that you will need to apply is the following:
```
curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -
sudo apt install -y gcc g++ make build-essential nodejs sox gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps
npm config set user root && sudo npm install edge-impulse-linux -g --unsafe-perm
```

then you will need to get intalled the edge implse linux python SDK 
```
sudo apt-get install libatlas-base-dev libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
pip3 install edge_impulse_linux -i https://pypi.python.org/simple
```

by doing this you will finally applu 
```
edge-impulse-linux-runner --download model.eim
```

After this installation, the python code will need to make the ML model to identify a vehicule, measure the speed of the vehicule and show it into a window to know the specification of this. 

For this part, the following code will display the the data collected by the OPS sensor
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

When you have already all the information installed, then we have to pass to the part of connecting a camera to the raspberry pi, on our case we use a web-cam taht connects via usb, for the case of the raspberry pi 4 you will need to have a camera that conects on usb 3.0 for this to work correct. 

&&&&& jp mete aca el programa que usa la camara &&

After using this program, we 

   

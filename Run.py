import socket
import serial as seri
from time import sleep

import cv2
import numpy as np
import time
import argparse
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument(
	'-m',
	'--model_file',
	default='./mymodel.tflite',
	help='.tflite model to be executed')
args = parser.parse_args()

COMMENT = 'OFF';

SOCKPATH = "/var/run/lirc/lircd"

sock = None

#Model input size
width = 150
height = 150

#Expected Accuracy
acc = 0.9

#Load Tensorflow Lite
import tflite_runtime.interpreter as tflite
interpreter = tflite.Interpreter(model_path=args.model_file)
interpreter.allocate_tensors()
inputdets = interpreter.get_input_details()
outputdets = interpreter.get_output_details()

# Establish a socket connection to the lirc daemon
def init_irw():
    global sock
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SOCKPATH)
    if(COMMENT == 'ON'):
        print ('Socket connection established!')
        print ('Ready...')

# parse the output from the daemon socket
def getKey():
    while True:
        data = sock.recv(128)
        data = data.strip()
        
        if (len(data) > 0):
            break
    
    words = data.split()
    return words[2], words[1]

# Main entry point
# The try/except structures allows the users to exit out of the program
# with Ctrl + C. Doing so will close the socket gracefully.

if __name__ == '__main__':
    try:
        init_irw()
        ser = seri.Serial('/dev/ttyACM0', 57600, timeout=1)
        global key_x;
        global key_y;
        global key_acc;
        key_x = 1;
        key_y = 1;
        key_acc = 10;
        MUL = 10;
        crack_flag = 0;
        dic_y = {'BTN_0' : 0, 'BTN_1' : 1,'BTN_2' : 2};
        dic_x = {'BTN_3' : 0, 'BTN_4' : 1,'BTN_5' : 2};
        dic_acc = {'KEY_0' : 0, 'KEY_1' : 1, 'KEY_2' : 2, 'KEY_3' : 3, 'KEY_4' : 4, 
                    'KEY_5' : 5, 'KEY_6' : 6, 'KEY_7' : 7, 'KEY_8' : 8, 'KEY_9' : 9};
        while True:

            
            #if(key_x == 1 and key_y == 1):
            #Stop
            #ser.write(str(0 * 10 * key_acc) + " " +  str(0 * 10 * key_acc));
                #print("STOP" + str(0 * 10 * key_acc) + " " + str(0 * 10 * key_acc));
                
            #Initialize time
            start_time = time.time()
            tmp_time = time.time()
            
#             key, dir = getKey();
#             key = key.decode(); # This variable contains the name of$
#             dir = dir.decode(); # This variable contains the directi$
#             # Only print the name when the key is pressed (and not released)
#             if(key in dic_x) :
#                 key_x = dic_x[key];
#             elif(key in dic_y) :
#                 key_y = dic_y[key];
#             elif(key in dic_acc) :
#                 key_acc = dic_acc[key];
#             else :
#                 print("No Signal")
            
            #Taek Picture
            subprocess.run(['raspistill', '-vf','-o','test.jpg', '-w', '640', '-h', '480', '-t', '10'], capture_output=False)
            
            if(COMMENT == 'ON'):
                print("Capture!")
                
            #TAKE PICTURE time

            stop_time = time.time()
            if(COMMENT == 'ON'):
                print('time: {:.3f}ms'.format((stop_time - tmp_time) * 1000) +"<br>")
            tmp_time = time.time()
            
            #Read image
            img = cv2.imread('./test.jpg')

            #Crop Ratio
            sli_width = int(img.shape[0] / width) - 1;
            sli_height = int(img.shape[1] / height) - 1;

            #SetGray
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            #Resize Image
            resize_Img = cv2.resize(img,(width * sli_width, height * sli_height))
            
            crack = 0
            
            #RESIZE TIME
            stop_time = time.time()
            if(COMMENT == 'ON'):
                print('time: {:.3f}ms'.format((stop_time - tmp_time) * 1000) +"<br>")
            tmp_time = time.time()
            
            #Loop -> sli_width * sli_height
            for i in range(1, sli_width + 1):
                for j in range(1, sli_height + 1):

                    #Get X location
                    x1 = (j - 1) * width
                    x2 = j * width

                    #Get Y location
                    y1 = (i - 1) * width
                    y2 = i * width

                    #Set input data
                    input_img = resize_Img[x1 : x2 , y1 : y2].copy()
                    input_data = np.array([input_img/255],dtype=np.float32)

                    #If gray : Set this option
                    input_data = input_data[...,np.newaxis]

                    #Use for debug
                    #print(input_data.shape)

                    #Get Result
                    interpreter.set_tensor(inputdets[0]['index'], input_data)
                    interpreter.invoke()
                    result = interpreter.get_tensor(outputdets[0]['index'])

                    #Compare result and expected accuracy
                    if(COMMENT == 'ON'):
                        print("Result : " + str(result) + "<br>")
                    if(result > acc):
                        if(COMMENT == 'ON'):
                            print("( " + str(i) + " ," + str(j) + ") is Crack<br>:")
                        crack = crack + 1
                    else:
                        if(COMMENT == 'ON'):
                            print("( " + str(i) + " ," + str(j) + ") is not  Crack<br>")
            
            subprocess.run(['rm', '-rf','test.jpg'], capture_output=False)

            if(crack > 1):
                MUL = 3
            else:
                MUL = 5
                
            #MODEL time
            stop_time = time.time()
            if(COMMENT == 'ON'):
                print('time: {:.3f}ms'.format((stop_time - tmp_time) * 1000) +"<br>")
            tmp_time = time.time()
            if(COMMENT == 'ON'):    
                print(str(crack))

#             if(key_x == 1 and key_y == 0):
#                 #STOP
#                 ser.write(str.encode(str(0 * MUL * key_acc) + " " +  str(0 * MUL * key_acc) + "\n"));
#                 if(COMMENT == 'ON'):
#                     print("BACK : " + str(0 * MUL * key_acc) + " " + str(0 * MUL * key_acc));
#             elif(key_x == 1 and key_y == 2):
#                 #Move Forward
#                 ser.write(str.encode(str(1 * MUL * key_acc) + " " +  str(1 * MUL * key_acc) + "\n"));
#                 if(COMMENT == 'ON'):
#                     print("FORWARD : " + str(1 * MUL * key_acc) + " " + str(1 * MUL * key_acc));
#             elif(key_x == 0 and key_y == 1):
#                 #Move Left
#                 ser.write(str.encode(str(0 * MUL * key_acc) + " " +  str(1 * MUL * key_acc) + "\n"));
#                 if(COMMENT == 'ON'):
#                     print("LEFT : " + str(0 * MUL * key_acc) + " " + str(1 * MUL * key_acc));
#             elif(key_x == 2 and key_y == 1):
#                 #Move Right
#                 ser.write(str.encode(str(1 * MUL * key_acc) + " " +  str(0 * MUL * key_acc) + "\n"));
#                 if(COMMENT == 'ON'):
#                     print("RIGHT : " + str(1 * MUL * key_acc) + " " + str(0 * MUL * key_acc));
#             elif(key_x == 2 and key_y == 2):
#                 #Move Forward & Right
#                 ser.write(str.encode(str(1 * MUL * key_acc) + " " +  str(0.5 * MUL * key_acc) + "\n"));
#                 if(COMMENT == 'ON'):
#                     print("FORWARD / RIGHT : " + str(1 * MUL * key_acc) + " " + str(0.5 * MUL * key_acc));
#             elif(key_x == 2 and key_y == 0):
#                 #STOP
#                 ser.write(str.encode(str(0 * MUL * key_acc) + " " +  str(0 * MUL * key_acc) + "\n"));
#                 if(COMMENT == 'ON'):
#                     print("BACK / : " + str(0 * MUL * key_acc) + " " + str(0 * MUL * key_acc));
#             elif(key_x == 0 and key_y == 2):
#                 #Move Forward & Left
#                 ser.write(str.encode(str(0.5 * MUL * key_acc) + " " +  str(1 * MUL * key_acc) + "\n"));
#                 if(COMMENT == 'ON'):
#                     print("FORWARD / LEFT : " + str(0.5 * MUL * key_acc) + " " + str(1 * MUL * key_acc));
#             elif(key_x == 0 and key_y == 0):
#                 #STOP
#                 ser.write(str.encode(str(0 * MUL * key_acc) + " " +  str(0 * MUL * key_acc) + "\n"));
#                 if(COMMENT == 'ON'):
#                     print("BACK // : " + str(0 * MUL * key_acc) + " " + str(0 * MUL * key_acc));
#             else:

            ser.write(str.encode(str(1 * MUL * key_acc) + " " +  str(1 * MUL * key_acc) + "\n"));
            if(MUL == 3):
                print("CRACK!")
                sleep(9)
            #Get time
            stop_time = time.time()
            if(COMMENT == 'ON'):
                print('time: {:.3f}ms'.format((stop_time - start_time) * 1000) +"<br>")
                
            sleep(0.01)
    except KeyboardInterrupt:
        ser.write(str.encode(str(0) + " " +  str(0) + "\n"));
        print ("\nShutting down...")
        # Close the socket (if it exists)
        if (sock != None):
            sock.close()
        print ("Done!")

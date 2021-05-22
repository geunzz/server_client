import time
import imagezmq
import cv2
import zmq
import threading

#connect to local ip
connect_ip_port = 'tcp://127.0.0.1:9999'
cap = cv2.VideoCapture(0)

class data_sender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sender = imagezmq.ImageSender(connect_to=connect_ip_port)
        self.sender.zmq_socket.RCVTIMEO = 3000
    def run(self):
        while True:
            try:
                _, frame = cap.read()
                frame = cv2.flip(frame, 1)
                image = frame
                image = cv2.resize(frame, dsize=(320, 240))
                message_from_server = self.sender.send_image(_, image)
                cv2.imshow('CLIENT_CAM', image)
            except zmq.error.Again:
                print('No response from server. Waiting for server connection..')
                cv2.waitKey(1)
                cv2.destroyWindow('CLIENT')
                self.sender.close()
                self.sender = imagezmq.ImageSender(connect_to=connect_ip_port)
                self.sender.zmq_socket.RCVTIMEO = 3000        
                continue

            if cv2.waitKey(1) == ord('q'):
                self.sender.send_image('q', image)
                time.sleep(0.3)
                break

            elif message_from_server == b'q' or message_from_server == b'Q':
                cv2.waitKey(1)
                cv2.destroyWindow('CLIENT')
                break

if cap.isOpened():
    transfer = data_sender()
    transfer.start()

            

    

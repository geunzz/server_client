import cv2
import imagezmq
import time
import threading
import zmq

#define two image hub module
image_hub1 = imagezmq.ImageHub(open_port='tcp://*:9998')
image_hub2 = imagezmq.ImageHub(open_port='tcp://*:9999')

#client module class
class module(threading.Thread):
    def __init__(self, image_hub, client):
        self.stopped = False
        threading.Thread.__init__(self)
        self.flag_timeout = False
        self.flag_connection_msg = True
        self.image_hub = image_hub
        self.client = client
    def stop(self):
        self.stopped = True
        message_stop = self.client + ' stopped'
        print(message_stop)
    
    def run(self):
        message_run = 'port for ' + self.client + ' is opened.'
        print(message_run)
        while self.stopped==False:
            try:
                self.message, image = self.image_hub.recv_image()
                self.image_hub.zmq_socket.RCVTIMEO = 3000 #timeout 3000ms
                cv2.imshow(self.client, image)
                if self.flag_connection_msg == True:
                    now = time.localtime()
                    message_connect = self.client + ' is connected to server :'
                    print(message_connect, "%04d/%02d/%02d %02d:%02d:%02d" % 
                    (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                    self.flag_connection_msg = False
            except zmq.error.Again:
                message_no_response = 'Timeout occured : No response from ' + self.client
                print(message_no_response)
                cv2.waitKey(1)
                cv2.destroyWindow(self.client)
                self.flag_timeout = True
                
            if self.flag_timeout == False:
                if str(self.message) == 'Q' or str(self.message) == 'q':
                    self.image_hub.send_reply(b'q')
                    time.sleep(0.3)
                    now = time.localtime()
                    message_quit = 'Quit message from ' + self.client
                    print(message_quit, "%04d/%02d/%02d %02d:%02d:%02d" % 
                    (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                    cv2.waitKey(1)
                    cv2.destroyWindow(self.client)
                    self.__init__(self.image_hub, self.client)
                    self.image_hub.zmq_socket.RCVTIMEO = -1
                    
                elif cv2.waitKey(1) == ord('q'):
                    self.image_hub.send_reply(b'q')
                    time.sleep(0.3)
                    now = time.localtime()
                    message_disconnect = 'Disconnect the ' + self.client
                    print(message_disconnect, "%04d/%02d/%02d %02d:%02d:%02d" % 
                    (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                    cv2.waitKey(1)
                    cv2.destroyWindow(self.client)
                    self.__init__(self.image_hub, self.client)
                    self.image_hub.zmq_socket.RCVTIMEO = -1
                else:
                    self.image_hub.send_reply(b'OK')
            else:
                self.flag_timeout ==  False
                self.__init__(self.image_hub, self.client)
                self.image_hub.zmq_socket.RCVTIMEO = -1

t1 = module(image_hub1,'client1')
t2 = module(image_hub2,'client2')

t1.start()
t2.start()


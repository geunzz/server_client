# server_client
This code implements the function of sending and receiving images between the client and the server using the imagezmq library. 
You can specify the number of ports to open on the server, and it is implemented to open two ports (9999, 9998) as an example in the current code. 
If there is no response from the client for 3000ms(User can change it to their liking) timeout, 
the server automatically terminates the image reception and terminates the connection with the client.
Since the port remains open, other clients can connect to the same port in the future.
In addition, the server and the client can terminate the connection by pressing the'q' button in the image displayed respectively.    
You can find more information about the imagezmq library at this address : https://github.com/jeffbass/imagezmq

  
How to use
---------------------------------------------------
First of all, install the necessary libraries, including imagezmq.  
  
    pip install -r requirements.txt  
    
If you run the server as shown below, you can access the ip address and port of the computer running the code.

    python imagezmq_server.py   
    
You can connect to the server by executing the client code while the server is running. 
At this time, the IP of the computer running the server and the designated port must be correctly set.  

    python imagezmq_client.py  
    
If both the server and client code are run on the same computer, you can set the IP address designation value in the client code to the local address as shown below. 

    connect_ip_port = 'tcp://127.0.0.1:9999'  

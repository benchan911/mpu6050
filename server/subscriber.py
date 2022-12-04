import paho.mqtt.client as mqtt
from statistics import stdev

# 16384
AcX_list = []
AcY_list = []
AcZ_list = []

prev_x, prev_y, prev_z = 0, 0, 0 
dist_x, dist_y, dist_z = 0, 0, 0
flag_x, flag_y, flag_z = False, False, False

def process_data(msg):
    global AcX_list
    msg = msg[1:-1]
    print(msg)
    d = msg.split(",")
    data = (int(d[0])/16384, int(d[1])/16384, int(d[2])/16384)
    #print(data[1:-1])
    return data

def on_message(client, userdata, message):
    global prev_x, prev_y, prev_z
    global dist_x, dist_y, dist_z 
    global flag_x, flag_y, flag_z
    e = 1
    size = 100
    t = 1
    f = True
    m = str(message.payload.decode("utf-8"))
    #print("received message: " , m)
    x, y, z = process_data(m)
    if len(AcX_list) < size:
        AcX_list.append(x)
        AcY_list.append(y)
        AcZ_list.append(z)
        print("Loading Data..")
    else:
        AcX_stdev = stdev(AcX_list)
        AcY_stdev = stdev(AcY_list)
        AcZ_stdev = stdev(AcZ_list)

        AcX_delta = abs(x-prev_x)
        AcY_delta = abs(y-prev_y)
        AcZ_delta = abs(z-prev_z)
        print("STDEV: {}, {}, {}".format(round(AcX_stdev,2), round(AcY_stdev,2), round(AcZ_stdev,2)))
        print("Delta: {}, {}, {}".format(round(AcX_delta,2), round(AcY_delta,2), round(AcZ_delta,2)))

        if abs(x-prev_x) > AcX_stdev*e:
            if flag_x or f:
                dist_x += 0.5*((x-prev_x)*9.8)*(t**2)
            flag_x = True
        else:
            flag_x = False

        if abs(y-prev_y) > AcY_stdev*e:
            if flag_y or f:
                dist_y += 0.5*((y-prev_y)*9.8)*(t**2)
            flag_x = True
        else: 
            flag_x = False
            
        if abs(z-prev_z) > AcZ_stdev*e:
            if flag_z or f:
                dist_z += 0.5*((z-prev_z)*9.8)*(t**2)
            flag_x = True
        else:
            flag_x = False

        print("X =", round(dist_x, 2))
        print("Y =", round(dist_y, 2))
        print("Z =", round(dist_z, 2))
        print("-"*10)    
    
    prev_x = x
    prev_y = y
    prev_z = z
        
        
    
    




mqttBroker ="192.168.68.105" 


client = mqtt.Client("Blue")
client.connect(mqttBroker) 

client.subscribe("DISPLACEMENT")
client.on_message=on_message 

client.loop_forever()
    
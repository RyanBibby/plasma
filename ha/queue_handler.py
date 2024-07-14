from umqtt.simple import MQTTClient

def sub(topic, msg):
    global r, g, b, brightness, status

    stopic = topic.decode("utf-8")
    smsg = msg.decode("utf-8")
    
    if stopic == rgb_command_topic:
        print("RGB")
        print(smsg)
        tr,tg,tb = (smsg.split(","))
        r = int(int(tr) / 4)
        g = int(int(tg) / 4)
        b = int(int(tb) / 4)
    elif stopic == brightness_command_topic:
        brightness = float(smsg)/255
    elif stopic == command_topic:
        print("Command")
        print(smsg)
        if smsg == "ON":
            status = True
        else:
            status = False 

class QueueHander:
    queue = None

    def __init__(self, topic_prefix):

        self.command_topic = f'{topic_prefix}/switch'
        self.state_topic = f'{topic_prefix}/state'
        self.brightness_command_topic = f'{topic_prefix}/brightness/set'
        self.rgb_command_topic = f'{topic_prefix}/color/set'

        self.client = MQTTClient('LED Strip', '192.168.1.88', 1883, 'ryan', 'panda')
        self.client.set_callback(sub)
        self.client.connect()
        self.client.subscribe(f'{topic_prefix}/#')

    def get_state():
        return status
    
    def publish_state(message):
        self.client.publish(self.state_topic, "ON")


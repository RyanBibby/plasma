from umqtt.simple import MQTTClient

class QueueHander:

    def __init__(self, topic_prefix, strip):

        self.command_topic = f'{topic_prefix}/switch'
        self.state_topic = f'{topic_prefix}/state'
        self.brightness_command_topic = f'{topic_prefix}/brightness/set'
        self.rgb_command_topic = f'{topic_prefix}/color/set'

        self.client = MQTTClient('LED Strip', '192.168.1.88', 1883, 'ryan', 'panda')
        self.client.set_callback(self.sub)
        self.client.connect()
        self.client.subscribe(f'{topic_prefix}/#')

        self.strip = strip

        self.client.publish(self.state_topic, "ON")

    def sub(self, topic, msg):
        stopic = topic.decode("utf-8")
        smsg = msg.decode("utf-8")
        
        if stopic == self.rgb_command_topic:
            tr,tg,tb = (smsg.split(","))
            r = int(int(tr) / 4)
            g = int(int(tg) / 4)
            b = int(int(tb) / 4)
        elif stopic == self.brightness_command_topic:
            brightness = float(smsg)/255
        elif stopic == self.command_topic:
            if smsg == "ON":
                self.strip.turn_on()
                self.publish_state("ON")
            else:
                self.strip.turn_off()
                self.publish_state("OFF")

    def publish_state(self,message):
        print("Publishing off")
        self.client.publish(self.state_topic, message)

    def check(self):
        self.client.check_msg()
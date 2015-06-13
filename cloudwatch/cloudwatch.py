import boto.ec2.cloudwatch

# The channels are set in rtmbot.conf
BOTS_CHANNEL = None
ALARM_CHANNEL = None

# The following three actually live in the Plugin class in rtmbot.py
crontable = []
outputs = []
config = None

# This is our connection to EC2 CloudWatch
connection = None


def setup():
    global connection, BOTS_CHANNEL, ALARM_CHANNEL

    connection = boto.ec2.cloudwatch.connect_to_region('eu-west-1')

    BOTS_CHANNEL = config['bots_channel']
    ALARM_CHANNEL = config['alarm_channel']

    alarm_check_interval = 60
    if 'alarm_check_interval' in config:
        alarm_check_interval = config['alarm_check_interval']

    print(alarm_check_interval)
    crontable.append([alarm_check_interval, "check_alarms"])


def process_message(data):
    channel = data['channel']
    if 'subtype' not in data.keys():
        text = data['text']
        if 'get alarms' in text:
            get_alarms(channel)


def get_alarms(channel):
    alarms = connection.describe_alarms()
    outputs.append([channel, format_alarms(alarms)])


def check_alarms():
    alarms = connection.describe_alarms()
    active_alarms = [a for a in alarms if a.state_value != 'OK']
    if len(active_alarms) > 0:
        message = format_alarms(alarms)
        outputs.append([BOTS_CHANNEL, message])
        if BOTS_CHANNEL != ALARM_CHANNEL:
            outputs.append([ALARM_CHANNEL, message])
    else:
        # TODO: Remove this when development is done, because it is spammy!
        print("All alarms are OK")


def format_alarms(alarms):
    alarm_strings = ['>{}: *{}*'.format(a.name, a.state_value) for a in alarms]
    return '\n'.join(alarm_strings)

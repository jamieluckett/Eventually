import configparser

CONFIG_LOCATION = 'config.cfg' 
config = configparser.ConfigParser()
config.read(CONFIG_LOCATION)

EVENT_NAME_LENGTH = int(config['EVENT']['EVENT_NAME_LENGTH'])
EVENT_KEY_LENGTH = int(config['EVENT']['EVENT_KEY_LENGTH'])
EVENT_MAX_GUESTS = int(config['EVENT']['EVENT_MAX_GUESTS'])

GUEST_FIRSTNAME_LENGTH = int(config['GUEST']['GUEST_FIRSTNAME_LENGTH'])
GUEST_SURNAME_LENGTH = int(config['GUEST']['GUEST_SURNAME_LENGTH'])
GUEST_EMAIL_LENGTH = int(config['GUEST']['GUEST_EMAIL_LENGTH'])

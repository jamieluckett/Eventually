import configparser

CONFIG_LOCATION = 'config.cfg'
EMAIL_CONFIG_LOCATION = 'email_config.cfg'

config = configparser.ConfigParser()
email_config = configparser.ConfigParser()
config.read(CONFIG_LOCATION)
email_config.read(EMAIL_CONFIG_LOCATION)

EVENT_NAME_LENGTH = int(config['EVENT']['EVENT_NAME_LENGTH'])
EVENT_KEY_LENGTH = int(config['EVENT']['EVENT_KEY_LENGTH'])
EVENT_MAX_GUESTS = int(config['EVENT']['EVENT_MAX_GUESTS'])
EVENT_DESCRIPTION_LENGTH = int(config['EVENT']['EVENT_DESCRIPTION_LENGTH'])

GUEST_FIRSTNAME_LENGTH = int(config['GUEST']['GUEST_FIRSTNAME_LENGTH'])
GUEST_SURNAME_LENGTH = int(config['GUEST']['GUEST_SURNAME_LENGTH'])
GUEST_EMAIL_LENGTH = int(config['GUEST']['GUEST_EMAIL_LENGTH'])

GROUP_NAME_LENGTH = str(config['GROUP']['GROUP_NAME_LENGTH'])

EVENT_DEFAULT_DESCRIPTION = str(config['TEMPORARY']['EVENT_DESCRIPTION'])

SITE_URL = str(config['SITE']['URL'])

SUBJECT_TEMPLATE = str(config['EMAIL']['SUBJECT_TEMPLATE'])

DOMAIN = str(config['OTHER']['DOMAIN'])

#EMAIL

EMAIL_SERVER = str(email_config['EMAIL']['SERVER'])
EMAIL_PORT = int(email_config['EMAIL']['PORT'])
EMAIL_ADDRESS = str(email_config['EMAIL']['ADDRESS'])
EMAIL_PASSWORD = str(email_config['EMAIL']['PASSWORD'])
EMAIL_LOOP_INTERVAL = int(email_config['EMAIL']['EMAIL_LOOP_INTERVAL'])

from ippanel import Client

from payamchi.settings import SMS_CONFIG

ORIGINATOR: str = SMS_CONFIG['ORIGINATOR']
API_KEY: str = SMS_CONFIG['API_KEY']


def send(message: str, recipients: str):
    sms = Client(API_KEY)

    bulk_id = sms.send_pattern(
        pattern_code='eop4wh5107aydjw',
        recipient=recipients,
        originator=ORIGINATOR,
        values={'verification-code': message}

    )

    #     sms.send(
    #     ORIGINATOR,
    #     recipients,
    #     message,
    # )
    return bulk_id

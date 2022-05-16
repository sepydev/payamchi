from ippanel import Client

from payamchi.payamchi.settings import SMS_CONFIG


class SmsSender:
    ORIGINATOR: str = SMS_CONFIG['ORIGINATOR']
    API_KEY: str = SMS_CONFIG['ORIGINATOR']

    def send(self, message: str, recipients: list[str]):
        sms = Client(self.api_key)
        bulk_id = sms.send(
            self.originator,
            recipients,
            message,
        )
        return bulk_id

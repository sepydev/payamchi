import secrets
import string

from payamchi.settings import CONFIRM_CODE_LENGTH


def get_secret_code():
    secret_code = ''.join(
        secrets.choice(string.digits) for _ in range(CONFIRM_CODE_LENGTH)
    )
    return secret_code
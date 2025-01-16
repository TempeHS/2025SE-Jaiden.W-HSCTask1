import pyotp
import qrcode
import io
from base64 import b64encode

def generate_totp_secret():
    return pyotp.random_base32()

def get_totp_uri(secret, username, issuer_name="DevLogs"):
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(username, issuer_name=issuer_name)

def generate_qr_code(uri):
    qr = qrcode.make(uri, box_size=8)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    return b64encode(buf.getvalue()).decode('utf-8')

def verify_totp(token, secret):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
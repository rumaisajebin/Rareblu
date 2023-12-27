import pyotp
from datetime import datetime, timedelta
from django.core.mail import EmailMessage


def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_key'] = totp.secret
    otp_valid = datetime.now() + timedelta(minutes=10)
    request.session['otp_valid'] = str(otp_valid)
    print(otp_valid)
    print(f"Your otp is {otp}")

    mail = request.session['email']
    subject = 'Verify your account please'
    msg = f"Verify your account by this otp: {otp}"
    frm = 'jebinrumaisa@gmail.com'
    to = [mail]

    try:
        email = EmailMessage(subject, msg, frm, to)
        email.send()
    except Exception as e:
        print(f"Failed to send OTP: {str(e)}")
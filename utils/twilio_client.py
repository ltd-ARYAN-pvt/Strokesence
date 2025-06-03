from dotenv import load_dotenv
from twilio.rest import Client
from config import settings

try:
    client = Client(settings.ACC_SID, settings.Auth_token)
except Exception as e:
    print(e)

def send_emergency_sms(phone, user):
    body_message = (
        f"🚨 Emergency Alert: {user} may be experiencing stroke symptoms. "
        "Please check on them immediately or call emergency services!"
    )
    try:
        client.messages.create(
            from_ ='+19472106154',
            body=body_message,
            to=phone
        )
    except Exception as e:
        print(f"Exception Occured, {e}")

def send_emergency_whatsapp_msg(phone, user):
    body_message = (
        f"🚨 Emergency Alert: {user} may be experiencing stroke symptoms. "
        "Please check on them immediately or call emergency services!"
    )
    # print(user, phone)
    try:
        client.messages.create(
            from_=f'whatsapp:{settings.MT_Whatsapp}',
            body=body_message,
            to=f'whatsapp:+919555699400'
        )
    except Exception as e:
        print(f"Exception Occured, {e}")
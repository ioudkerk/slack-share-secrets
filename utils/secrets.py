import redis
import uuid
from cryptography.fernet import Fernet
from config import REDIS_HOST, REDIS_PORT, ENCRYPT_KEY, PASSWD_TTL

if not ENCRYPT_KEY:
    ENCRYPT_KEY=Fernet.generate_key()

def getsecret(uuid):
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)        
        f = Fernet(ENCRYPT_KEY)
        key_encoded = r.get(uuid)
        r.delete(uuid)
        token = f.decrypt(key_encoded)
        return token.decode('utf-8')
    except:
        return "No secrets to read"

def gen_one_time_url(text):
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    passwd_uuid = str(uuid.uuid4())
    f = Fernet(ENCRYPT_KEY)
    token = f.encrypt(text.encode('utf-8'))
    r.set(passwd_uuid, token, ex=PASSWD_TTL)
    return passwd_uuid
import string
import secrets


def create_url(target_url):
    alphabet = string.ascii_uppercase + string.digits
    key = ''.join(secrets.choice(alphabet) for _ in range(5))
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(10))
    shortened_url = base_url + key
    return shortened_url


base_url = "http://127.0.0.1:8000/"
print(create_url('google.com'))

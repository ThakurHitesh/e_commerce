import secrets, string

def generate_random_password():
    """
    generate random password
    """
    return ''.join(secrets.choice(string.ascii_lowercase + string.digits) 
                                                  for i in range(10)) 
def generate_random_username():
    """
    generate random username
    """
    return ''.join(secrets.choice(string.ascii_lowercase) for i in range(14))

def generate_otp():
    """
    generate otp for user
    """
    return ''.join(secrets.choice(string.digits) for i in range(4))


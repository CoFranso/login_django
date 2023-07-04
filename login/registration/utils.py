# IMPORTS

# Methods

def get_email_provider(email):
    domain = email.split('@')[-1].lower()

    if domain in ['outlook.com', 'hotmail.com', 'live.com']:
        return "live.com"
    elif domain == "yahoo.com":
        return "mail.yahoo.com"
    elif domain in ['icloud.com', 'me.com', 'mac.com']:
        return "mail.me.com"
    else:
        return domain

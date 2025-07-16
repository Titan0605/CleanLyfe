import secrets
def generate_token(n_bytes=16):
    return secrets.token_hex(n_bytes)
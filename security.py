from pwdlib import PasswordHash
password_hash=PasswordHash.recommended()
def hash_password(plain_password):
    return password_hash.hash(plain_password)
def verify_password(plain_password,hash_password):
    return password_hash.verify(plain_password,hash_password)    

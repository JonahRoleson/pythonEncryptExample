from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# === Load Symmetric Key (Fernet) ===
with open("symmetric.key", "rb") as f:
    SYMMETRIC_KEY = f.read().strip()

fernet = Fernet(SYMMETRIC_KEY)

# === Load RSA Keys (PEM files) ===
with open("rsa_public.pem", "rb") as f:
    PUBLIC_KEY_PEM = f.read()
with open("rsa_private.pem", "rb") as f:
    PRIVATE_KEY_PEM = f.read()

public_key = serialization.load_pem_public_key(PUBLIC_KEY_PEM)
private_key = serialization.load_pem_private_key(PRIVATE_KEY_PEM, password=None)

# --- Symmetric demo ---
print("=== Symmetric Encryption (Fernet) ===")
msg = input("Enter message for symmetric encryption: ").encode()
ct = fernet.encrypt(msg)
pt = fernet.decrypt(ct)

print("\n[Symmetric] Key (Base64):")
print(SYMMETRIC_KEY.decode())
print("[Symmetric] Ciphertext:")
print(ct.decode())
print("[Symmetric] Decrypted:")
print(pt.decode())

# --- Asymmetric demo ---
print("\n=== Asymmetric Encryption (RSA-OAEP) ===")
msg = input("Enter message for asymmetric encryption: ").encode()
ct = public_key.encrypt(
    msg,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
pt = private_key.decrypt(
    ct,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("\n[Asymmetric] Public Key PEM:\n")
print(PUBLIC_KEY_PEM.decode())
print("\n[Asymmetric] Private Key PEM:\n")
print(PRIVATE_KEY_PEM.decode())
print("\n[Asymmetric] Ciphertext:", ct)
print("[Asymmetric] Decrypted:", pt.decode())

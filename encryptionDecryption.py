from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

print("=== Symmetric Encryption ===")
user_key = input("Enter a symmetric key (Base64) or leave blank to generate one: ").strip()

if user_key:
    sym_key = user_key.encode()
else:
    sym_key = Fernet.generate_key()
    print(f"No key provided, generated: {sym_key.decode()}")

cipher = Fernet(sym_key)

message = input("Enter a message for symmetric encryption: ").encode()
ciphertext = cipher.encrypt(message)
plaintext = cipher.decrypt(ciphertext)

print(f"\nSymmetric Key: {sym_key.decode()}")
print(f"Ciphertext: {ciphertext.decode()}")
print(f"Decrypted: {plaintext.decode()}")

print("=== Asymmetric Encryption ===")

choice = input("Do you want to (1) provide keys or (2) generate new ones? [1/2]: ").strip()

if choice == "1":
    priv_pem = input("Paste your RSA PRIVATE key (PEM format, single line \\n for newlines):\n")
    pub_pem = input("Paste your RSA PUBLIC key (PEM format, single line \\n for newlines):\n")

    private_key = serialization.load_pem_private_key(
        priv_pem.encode().replace(b"\\n", b"\n"),
        password=None,
    )
    public_key = serialization.load_pem_public_key(
        pub_pem.encode().replace(b"\\n", b"\n")
    )
else:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    print("Generated new RSA keys.")

message = input("Enter a message for asymmetric encryption: ").encode()
ciphertext= public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("\nPublic Key PEM:\n", public_key.public_bytes( encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode())

print("\nPrivate Key PEM:\n", private_key.private_bytes( encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()).decode())

print(f"\nCiphertext: {ciphertext}...")
print(f"Decrypted: {plaintext.decode()}")

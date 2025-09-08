# **Crypto Demo — Symmetric (Fernet) & Asymmetric (RSA-OAEP)**

## **Overview**

This demo shows the **basics of encryption and decryption** using:

* **Fernet (symmetric)** — one shared key for encrypt/decrypt.

* **RSA-OAEP (asymmetric)** — public key encrypts, private key decrypts.

It prompts for messages at the terminal, encrypts them, then decrypts to verify correctness, and prints the keys used (Fernet Base64 key; RSA PEMs).

## **Files**

* `basic_crypto_demo_files.py` — main script (loads keys from files, prints PEMs).

* `symmetric.key` — Base64 Fernet key (44 chars).

* `rsa_public.pem` — RSA public key (PEM).

* `rsa_private.pem` — RSA private key (PEM).

## **Prerequisites**

* Python 3.9+

`cryptography`

 pip install -r requirements.txt

## **How to Run**

Place the three key files in the same directory as the script, then:

python encryptionDecryption.py

Follow the prompts to enter a symmetric message and an asymmetric message.

## **How It Works (High Level)**

### **Symmetric: Fernet**

* **Key:** a single Base64 string shared by both parties.

* **Encrypt:** `ciphertext = Fernet(key).encrypt(plaintext)`

* **Decrypt:** `plaintext = Fernet(key).decrypt(ciphertext)`

* **Integrity:** Fernet includes authentication (HMAC) so tampering is detected.

* **Randomness:** Each encryption uses a fresh IV and timestamp, so ciphertext differs every run even for the same input.

### **Asymmetric: RSA-OAEP**

* **Keys:** a keypair — **public** key (shareable) and **private** key (secret).

* **Encrypt:** `ciphertext = public_key.encrypt(plaintext, OAEP(...))`

* **Decrypt:** `plaintext = private_key.decrypt(ciphertext, OAEP(...))`

* **Padding:** OAEP (with MGF1 \+ SHA-256) provides semantic security and prevents deterministic outputs.

* **Randomness:** OAEP uses random padding; ciphertext changes on every run.

## **Why Fernet and RSA-OAEP?**

* **Fernet**

  * Simplicity: single call to encrypt/decrypt — ideal for a clear, short demo.

  * **Authenticated encryption:** ensures both confidentiality **and** integrity out of the box.

  * Well-vetted recipe built on AES \+ HMAC with standardized token format.

* **RSA-OAEP**

  * Modern, secure padding for RSA (as opposed to legacy PKCS\#1 v1.5).

  * Incorporates randomness to prevent pattern leakage and chosen-plaintext attacks.

  * Standard choice for encrypting small messages or **wrapping** symmetric keys in hybrid designs.

## **Expected Behavior: “Why does ciphertext change?”**

Both Fernet and RSA-OAEP include **randomness** (IVs / nonces / random padding).  
 **Same key \+ same message** → **different ciphertexts** each run, but **always decrypts** to the original plaintext. This is by design for security.

## **Security Notes (Brief)**

* Demo keys are for learning only; never reuse in real systems.

* Keep `rsa_private.pem` secret; distribute only the public key.

* For large data, use **hybrid encryption**: generate a random symmetric key for the data, then encrypt that key with RSA-OAEP.

## **Troubleshooting**

* **“InvalidToken” (Fernet):** Key mismatch or corrupted token.

* **PEM load errors:** Ensure files contain full headers/footers (`-----BEGIN ...-----`) and Unix newlines.

* **Base64 key format:** Fernet keys are 44-character URL-safe Base64 strings ending with `=`.

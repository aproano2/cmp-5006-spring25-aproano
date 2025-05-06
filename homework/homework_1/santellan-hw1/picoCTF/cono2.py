from subprocess import run, PIPE

# Load the encrypted password
with open("password.enc", "r") as file:
    encrypted_password = int(file.read())

print("=== Phase 1: Recovering the Password ===\n")

print(f"Ciphertext (c) = {encrypted_password}\n")

# Get a known plaintext message from the user
plaintext_message = input("Enter a known message (m1): ")
m1_ascii = ord(plaintext_message)

print(f"Requesting encryption for message (m1): {plaintext_message}\n")
c1 = int(input("Enter the encrypted output from the oracle (c1 = E(m1)): "))

# Construct a modified ciphertext using RSA's homomorphic property
c2 = encrypted_password * c1
print(f"Requesting decryption for modified ciphertext (c2 = c * c1): {c2}\n")

# Get the decrypted output and convert from HEX
m2_hex = input("Enter decrypted value in HEX format (m2 = D(c2)): ")
m2 = int(m2_hex, 16)

# Recover the original password
password_int = m2 // m1_ascii
password = password_int.to_bytes(len(str(password_int)), "big").decode("utf-8").lstrip("\x00")

print(f"Recovered Password: {password}\n")
print("=" * 50)

print("=== Phase 2: Decrypting the Secret File ===\n")

# Use OpenSSL to decrypt the secret file with the recovered password
decryption_result = run(
    ["openssl", "enc", "-aes-256-cbc", "-d", "-in", "secret.enc", "-pass", f"pass:{password}"],
    stdout=PIPE, stderr=PIPE, text=True
)

print(decryption_result.stdout)

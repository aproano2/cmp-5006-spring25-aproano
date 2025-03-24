from pwn import *

context.log_level = 'critical'
p = remote("titan.picoctf.net", 59646)
p.recvuntil(b"decrypt.")
# Read forbidden ciphertext from password.enc
with open("password.enc") as file:
	c = int(file.read())
# Request encryption: send "E" then encrypt the number 2
p.sendline(b"E")
p.recvuntil(b"keysize): ")
p.sendline(b"\x02")
p.recvuntil(b"mod n) ")
c_a = int(p.recvline())
# Request decryption: send "D" then the blinded ciphertext (c_a * c)
p.sendline(b"D")
p.recvuntil(b"decrypt: ")
p.sendline(str(c_a * c).encode())
p.recvuntil(b"mod n): ")
# The server returns (2 * password) in hex, so divide by 2 to get the password
password = int(p.recvline(), 16) // 2
password = password.to_bytes(len(str(password))-7, "big").decode("utf-8")
print("Password:", password)

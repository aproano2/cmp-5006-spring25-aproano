from pwn import *

context.log_level='critical'
p = remote("titan.picoctf.net", 63413)

p.recvuntil(b"decrypt.")

with open("password.enc") as file:
    c = int(file.read())

p.sendline(b"E")
p.recvuntil(b"keysize): ")
p.sendline(b"\x02")
p.recvuntil(b"mod n) ")

c_a = int(p.recvline())

p.sendline(b"D")
p.recvuntil(b"decrypt: ")
p.sendline(str(c_a*c).encode())
p.recvuntil(b"mod n): ")

password = int(p.recvline(), 16) // 2
password = password.to_bytes(len(str(password))-7, "big").decode("utf-8")

print("Password:", password)

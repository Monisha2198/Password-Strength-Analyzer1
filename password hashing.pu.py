import hashlib

password = input("Enter your password: ")

# Encode and hash the password
hashed_password = hashlib.sha256(password.encode()).hexdigest()

print("SHA-256 Hashed Password:", hashed_password)

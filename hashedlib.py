import hashlib
import os

# Create the assets folder if it doesn't exist
os.makedirs("assets", exist_ok=True)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --------- SIGN UP ---------
original_password = input("Create your password: ")
hashed_password = hash_password(original_password)

# Save hashed password to a file inside 'assets' folder
with open("assets/saved_hashes.txt", "w") as f:
    f.write(hashed_password)
print("\n✅ Password hashed and saved successfully!\n")

# --------- LOGIN ---------
login_password = input("Enter your password to login: ")
hashed_login = hash_password(login_password)

# Read hashed password from file
with open("assets/saved_hashes.txt", "r") as f:
    stored_hash = f.read()

# Compare
if hashed_login == stored_hash:
    print("✅ Access granted. Password matched!")
else:
    print("❌ Access denied. Wrong password!")




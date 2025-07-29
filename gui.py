import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import hashlib
import os
from zxcvbn import zxcvbn

# Create folder if not exists
os.makedirs("assets", exist_ok=True)

# --- FUNCTION DEFINITIONS ---

# Hash function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Analyze strength
def analyze_strength():
    pwd = entry.get()
    result = zxcvbn(pwd)
    score = result['score']
    feedback = result['feedback']

    strength_label.config(text=f"Strength Score: {score}/4", fg="white")
    suggestion_label.config(text="Suggestion: " + (feedback['suggestions'][0] if feedback['suggestions'] else "Good password!"), fg="white")

# Save hash
def save_hash():
    pwd = entry.get()
    hashed = hash_password(pwd)
    with open("assets/saved_hashes.txt", "w") as f:
        f.write(hashed)
    messagebox.showinfo("Saved", "Password hash saved successfully!")
    hash_label.config(text=f"SHA-256 Hash: {hashed[:30]}...", fg="lightgreen")

# Verify
def verify_password():
    try:
        with open("assets/saved_hashes.txt", "r") as f:
            stored = f.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved password found.")
        return

    pwd = entry.get()
    if hash_password(pwd) == stored:
        result_label.config(text="✅ Password Matched!", fg="lightgreen")
    else:
        result_label.config(text="❌ Password Not Matched!", fg="red")

# Show/hide password function
def toggle_password():
    if show_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

# Export Report
def export_report():
    pwd = entry.get()
    hashed = hash_password(pwd)
    result = zxcvbn(pwd)
    score = result['score']
    feedback = result['feedback']
    suggestion = feedback['suggestions'][0] if feedback['suggestions'] else "Good password!"

    with open("assets/password_report.txt", "w") as f:
        f.write("Password Report Summary\n")
        f.write("-----------------------\n")
        f.write(f"Entered Password: {'*' * len(pwd)}\n")
        f.write(f"SHA-256 Hash: {hashed}\n")
        f.write(f"Strength Score: {score}/4\n")
        f.write(f"Suggestion: {suggestion}\n")

    messagebox.showinfo("Exported", "Password report saved to assets/password_report.txt")


# --- GUI DESIGN ---

root = tk.Tk()
root.title("🔐 Password Strength & Hash Tool")
root.geometry("430x460")
root.resizable(False, False)
# Load background image
bg_image = Image.open("assets/background.jpg")
bg_image = bg_image.resize((430, 460))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Styles
btn_style = {
    "font": ("Helvetica", 12, "bold"),
    "bg": "#4f5b66",
    "fg": "white",
    "activebackground": "#65737e",
    "activeforeground": "white",
    "width": 20,
    "bd": 0,
    "relief": "ridge",
    "pady": 5
}

tk.Label(root, text="Enter Password", font=("Helvetica", 14), bg="#2d2f33", fg="white").pack(pady=(20, 10))
entry = tk.Entry(root, show="*", font=("Helvetica", 12), width=30, bd=2, relief="groove")
entry.pack(pady=(0, 15))

# Show/Hide Password
show_var = tk.BooleanVar()
show_check = tk.Checkbutton(root, text="Show Password", variable=show_var, command=toggle_password,
                            bg="#2d2f33", fg="white", activebackground="#2d2f33", font=("Helvetica", 10))
show_check.pack(pady=(0, 15))

# Buttons
tk.Button(root, text="Check Strength", command=analyze_strength, **btn_style).pack(pady=6)
tk.Button(root, text="Hash and Save", command=save_hash, **btn_style).pack(pady=6)
tk.Button(root, text="Verify Password", command=verify_password, **btn_style).pack(pady=6)
tk.Button(root, text="Export Report", command=export_report, **btn_style).pack(pady=6)

# Labels
strength_label = tk.Label(root, text="", bg="#2d2f33", font=("Helvetica", 11))
strength_label.pack(pady=5)

suggestion_label = tk.Label(root, text="", bg="#2d2f33", font=("Helvetica", 10))
suggestion_label.pack(pady=5)

hash_label = tk.Label(root, text="", bg="#2d2f33", wraplength=380, justify="center", font=("Courier", 9))
hash_label.pack(pady=5)

result_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), bg="#2d2f33")
result_label.pack(pady=10)

root.mainloop()

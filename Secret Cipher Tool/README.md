# 🔐 Secret Cipher Tool

A custom encryption and decryption tool built with Python. This project uses unique string manipulation logic to transform plain text into a secure encoded format and vice versa.

## 🚀 How it Works
The tool follows a custom-built logic for security:
- **Encryption:** - If a word is 3 characters or longer, it removes the first letter, appends it to the end, and adds 3 random characters at the start and end.
  - If a word is less than 3 characters, it simply reverses the string.
- **Decryption:** - It reverses the encryption process by removing random characters and restoring the original word structure.

## 🛠️ Features
- **Custom Logic:** No external cryptography libraries used; purely logic-driven.
- **Randomized Padding:** Uses `random` module to generate unique noise for every encryption.
- **Efficiency:** Handles multi-word sentences using list comprehension and string slicing.

## 💻 Tech Stack
- **Language:** Python 3.x
- **Modules:** `random` (for noise generation), `string` (for character sets).

## 📖 Usage
1. Run the script:
   ```bash
   python app.py
2. Choose '1' for Coding (Encryption) or '0' for Decoding (Decryption).
3. Enter your message and get the result instantly!
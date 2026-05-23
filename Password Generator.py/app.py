import random
import string

def generate_password(length, use_number=True, use_symbol=True):
    """
    Generate a random password.
    :param length: Length of the password
    :param use_numbers: include digits if True
    :param use_symbols: include symbols if True
    :return: Generated password string
    """

    characters = string.ascii_letters
    if use_number:
        characters += string.digits
    
    if use_symbol:
        characters += string.punctuation

    if not characters:
        return ""
    
    password = "".join(random.choice(characters) for _ in range(length))
    return password
def main():
    """Main Program Execution"""
    print("\n🔒 Password Generator 🔒\n")
    try:
        length = int(input("Enter password length: "))
        if length <= 0:
            print("Password length must be greater than 0.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    include_numbers = input("Include numbers? (yes/no): ").lower() == "yes"
    include_symbols = input("Include symbols? (yes/no): ").lower() == "yes"
    
    password = generate_password(length,include_numbers,include_symbols)
    print("\n✅ Generated Password:")
    print(password)
if __name__ == "__main__":
    main()
from cryptography.fernet import Fernet


def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open("secret.key", "rb").read()



class cryptograph(object):

    def __init__(self):
        self.key = "R6r5uavzBZ0RMtbZZXpMjL4V3mjUpcoktVM5Dekc-J0="
        #self.key = load_key()

    def generate_key(self):
        """
        Generates a key and save it into a file
        """
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        """
        Load the previously generated key
        """
        return open("secret.key", "rb").read()

    def encrypt_message(self, message):
        """
        Encrypts a message
        """

        encoded_message = message.encode()
        f = Fernet(self.key)
        encrypted_message = f.encrypt(encoded_message)
        return encrypted_message


    def decrypt_message(self,encrypted_message):
        """
        Decrypts an encrypted message
        """
        f = Fernet(self.key)
        decrypted_message = f.decrypt(encrypted_message)
        return decrypted_message.decode()

if __name__ == '__main__':
    input = input("CreateKey or GetKey\n")

    if input == "CreateKey":
        generate_key()
    elif input == "GetKey":
        print(load_key())


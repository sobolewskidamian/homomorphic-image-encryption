from Pyfhel import Pyfhel, PyPtxt
from typing import List

from image_processor import ImageProcessor
from messages import ClientToServerData


class Client:
    def __init__(self) -> None:
        self.he = Pyfhel()
        self.he.contextGen(p=65537)
        self.he.keyGen()

    def encrypt_image(self, image_processor: ImageProcessor) -> ClientToServerData:
        print("Encrypting image...")
        client_encrypted_image: List[List[List[PyPtxt]]] = []
        for i, x_vector in enumerate(image_processor.image):
            x_vector_encrypted = []
            for pixel in x_vector:
                x_vector_encrypted.append(
                    [self.he.encryptFrac(rgb_value) for rgb_value in pixel]
                )
            client_encrypted_image.append(x_vector_encrypted)
            print(100 * i / len(image_processor.image))

        return ClientToServerData(
            client_encrypted_image,
            self.he.to_bytes_context(),
            self.he.to_bytes_publicKey(),
            image_processor.x_size,
            image_processor.y_size,
        )

    def decrypt_image(self, image: List[List[List[PyPtxt]]]) -> List[List[List[float]]]:
        print("Decrypting image...")
        decrypted_processed_image = []
        for i, x_vector in enumerate(image):
            decrypted_x_vector = []
            for pixel in x_vector:
                decrypted_x_vector.append(
                    [self.he.decryptFrac(rgb_value) for rgb_value in pixel]
                )
            decrypted_processed_image.append(decrypted_x_vector)
        return decrypted_processed_image

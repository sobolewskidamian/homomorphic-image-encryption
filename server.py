from Pyfhel import Pyfhel

from messages import ClientToServerData, ServerToClientData
from image_processor import EncryptedImageProcessor


class Server:
    def __init__(self, client_to_server_data: ClientToServerData) -> None:
        self.he = Pyfhel()
        self.he.from_bytes_context(client_to_server_data.context)
        self.he.from_bytes_publicKey(client_to_server_data.public_key)

        image = client_to_server_data.encrypted_image
        image_x = client_to_server_data.image_x
        image_y = client_to_server_data.image_y
        self._set_pyfhel(image)

        self.encrypted_image_processor = EncryptedImageProcessor(
            image, image_x, image_y
        )

    def _set_pyfhel(self, image) -> None:
        for x_vector in image:
            for pixel in x_vector:
                for rgb in pixel:
                    rgb._pyfhel = self.he

    def make_grey_scale(self) -> ServerToClientData:
        print("Processing image on server...")
        return ServerToClientData(self.encrypted_image_processor.make_grey_scale())

    def make_blur(self, blur_level: int = 10) -> ServerToClientData:
        print("Processing image on server...")
        return ServerToClientData(self.encrypted_image_processor.make_blur(blur_level))

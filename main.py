from image_processor import ImageProcessor
from client import ClientToServerData, Client
from server import ServerToClientData, Server

image_name = "image.png"
image_processor = ImageProcessor(image_name)
client = Client()

client_to_server_data: ClientToServerData = client.encrypt_image(image_processor)
server = Server(client_to_server_data)

server_to_client_data: ServerToClientData = server.make_grey_scale()
final_image = client.decrypt_image(server_to_client_data.encrypted_image)
image_processor.save_processed_image(final_image)

server_to_client_data: ServerToClientData = server.make_blur(15)
final_image = client.decrypt_image(server_to_client_data.encrypted_image)
image_processor.save_processed_image(final_image)

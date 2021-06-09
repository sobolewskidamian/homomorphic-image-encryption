from dataclasses import dataclass
from typing import List
from Pyfhel import PyPtxt


@dataclass
class ServerToClientData:
    encrypted_image: List[List[List[PyPtxt]]]


@dataclass
class ClientToServerData:
    encrypted_image: List[List[List[PyPtxt]]]
    context: bytes
    public_key: bytes
    image_x: int
    image_y: int

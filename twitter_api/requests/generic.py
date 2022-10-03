from typing import Dict


class TwitterRequest:
    def __init__(self, endpoint: str, parameters: Dict):
        self.endpoint = endpoint
        self.parameters = parameters

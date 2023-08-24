from base64 import b64decode
import requests


def get_data(block_number: int) -> list:
    """Метод для получения данных из блока в сети Akash. Принимает на вход
    номер блока, возвращает данные, хранящиеся по пути data.txs."""
    node_url: str = 'https://akash-rest.publicnode.com/blocks/'
    block_url: str = f'{node_url}{block_number}'
    response: requests.Response = requests.get(block_url)
    try:
        data_list: list = response.json().get('block').get('data').get('txs')
        return [b64decode(data) for data in data_list]
    except AttributeError:
        return f'No data available at block {block_number}'

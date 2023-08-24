import requests
import logging

from base64 import b64decode

logging.basicConfig(filename='py_log.log', level=logging.DEBUG,
                    filemode='w', force=True,
                    format='%(asctime)s %(levelname)s %(message)s')


def get_data(block_number: int) -> list | bool:
    """Method for receiving data from Akash Network.
    Takes block number as an input, returns the TXS stored
    in the data.txs path. Returns False if TXS data is empty,
    block number is invalid or node is unavailable."""
    node_url: str = 'https://akash-rest.publicnode.com/blocks/'
    block_url: str = f'{node_url}{block_number}'
    logging.info(f'Created block URL: {block_url}')

    try:
        response: requests.Response = requests.get(block_url)
    except requests.exceptions.ConnectionError as err:
        logging.warning(f'Node is unavailable: {node_url}; error text: {err}')
        return False
    logging.info('Successfully received response from the server..')

    block_data: list = response.json().get('block')

    if not block_data:
        logging.warning(f'Invalid block number #{block_number}')
        return False
    logging.info(f'Successfully received data from block #{block_number}')

    txs_list: list = block_data.get('data').get('txs')

    if not txs_list:
        logging.info(f'No TXS found in block {block_number}')
        return False

    logging.info(f'Successfully received TXS from block #{block_number}')
    return [b64decode(txs) for txs in txs_list]
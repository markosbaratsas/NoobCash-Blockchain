import hashlib
from json import dumps
from time import time
from typing import List

from .transaction import Transaction


class Block:
    """Blockchain block: Contains the transactions of a block of the
    blockchain. Also, contains other useful block data such as block index,
    block nonce, etc.
    """

    def __init__(self, index: int, nonce: int, previous_hash: str):
        """Block constructor: Inititalize a Block using given parameters

        Args:
            index (int): Block index (block serial number)
            nonce (str): Block nonce
            previous_hash (str): Previous block's hash
        """
        self.index = index
        self.timestamp = time()
        self.list_of_transactions = []
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.hash = self.__my_hash()

    def set_nonce(self, nonce: int):
        """Set nonce and update block's hash

        Args:
            nonce (int): The new nonce
        """
        self.nonce = nonce
        self.hash = self.__my_hash()
        
    def __my_hash(self):
        """Private function used to generate block's hash

        Returns:
            hash (str): Block's hash
        """
        obj = {
            "index": self.index,
            "timestamp": self.timestamp,
            "list_of_transactions": [str(x) for x in self.list_of_transactions],
            "nonce": self.nonce,
            "previous_hash": self.previous_hash
        }
        return hashlib.sha256(dumps(obj).encode('utf8')).hexdigest()

    def add_transactions_to_block(self, transactions: List[Transaction]):
        """Add Transaction to block's list of transactions

        Args:
            transaction (Transaction): The transaction to be added

        Returns:
            block (Block): The current block after the transaction insertion
        """
        for transaction in transactions:
            self.list_of_transactions.append(transaction)
        self.hash = self.__my_hash()
        return self

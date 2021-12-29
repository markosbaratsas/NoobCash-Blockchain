import hashlib
from json import dumps
from time import time

import blockchain
from transaction import Transaction


class Block:
    """Blockchain block: Contains the transactions of a block of the
    blockchain. Also, contains other useful block data such as block index,
    block nonce, etc.
    """

    def __init__(self, index: int, nonce: str, previousHash: str):
        """Block constructor: Inititalize a Block using given parameters

        Args:
            index (int): Block index (block serial number)
            nonce (str): Block nonce
            previousHash (str): Previous block's hash
        """
        self.index = index
        self.timestamp = time()
        self.listOfTransactions = []
        self.nonce = nonce
        self.previousHash = previousHash
        self.hash = self.__myHash()
        
        return self

    def __myHash(self):
        """Private function used to generate block's hash

        Returns:
            hash (str): Block's hash
        """
        obj = {
            "index": self.index,
            "listOfTransactions": self.listOfTransactions
        }
        return hashlib.sha256(obj.dumps.encode('utf-8')).hexdigest()
    
    def add_transaction(self, transaction: Transaction):
        """Add Transaction to block's list of transactions

        Args:
            transaction (Transaction): The transaction to be added

        Returns:
            block (Block): The current block after the transaction insertion
        """
        self.listOfTransactions.append(transaction)
        self.hash = self.__myHash()
        return self

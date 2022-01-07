from Crypto.Util.number import size
from .block import Block
from .transaction import Transaction

class Blockchain:
    """Blockchain: Blockchain that contains dict with blocks and other useful
    blockchain information
    """
    
    def __init__(self, capacity, difficulty):
        """Initialize the Blockchain

        Args:
            capacity (int): Blockchain's block capacity
            difficulty (str): The number of zeros to be found during mining
        """
        self.blockchain = {}
        self.last_block = None
        self.transactions = []
        self.capacity = capacity
        self.difficulty = difficulty

    def add_new_block(self, block: Block):
        """Add new block to blockchain. Insert into the `self.blockchain` dict
        the previous block (which has reached the max number of transactions),
        and keep new block to `self.last_block` variable.

        Args:
            block (Block): The new block to be assigned to `self.last_block`
                           variable

        Returns:
            blockchain (Blockchain): Blockchain after the insertion of a new
                                     block
        """
        self.blockchain[block.previous_hash] = self.last_block
        self.last_block = block
        return self

    def to_dict(self) -> dict:
        """Convert object to dict

        Args:
            None

        Returns:
            dict (dict): Object's dict
        """
        blockchain_to_dict = {}
        for hash, block in self.blockchain.items():
            blockchain_to_dict[hash] = block.to_dict()

        return {
            "blockchain": blockchain_to_dict,
            "last_block": self.last_block.to_dict,
            "transactions": [x.to_dict() for x in self.transactions],
            "capacity": self.capacity,
            "difficulty": self.difficulty
        }

    def parser(self, dictionary: dict) -> None:
        """Convert dictionary to object

        Args:
            dictionary (dict): The dictionary to be parsed
        """
        transactions = []
        for x in dictionary["transactions"]:
            transaction = Transaction("", "", "", 0, [])
            transaction.parser(x)
            transactions.append(transaction)

        last_block = Block(0, 0, "")
        last_block.parser(dictionary["last_block"])

        blockchain = {}
        for hash, block in self.blockchain.items():
            new_block = Block(0, 0, "")
            new_block.parser(block)
            blockchain[hash] = new_block

        self.capacity = dictionary["capacity"]
        self.difficulty = dictionary["difficulty"]
        self.transaction = transaction
        self.last_block = last_block
        self.blockchain = blockchain

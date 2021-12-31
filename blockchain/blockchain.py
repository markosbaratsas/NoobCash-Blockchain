from Crypto.Util.number import size
from .block import Block

class Blockchain:
    """Blockchain: Blockchain that contains dict with blocks and other useful
    blockchain information
    """
    
    def __init__(self, capacity, difficulty):
        """Initialize the Blockchain

        Returns:
            blockchain (Blockchain): Blockchain with the genesis block
        """
        self.blockchain = {}
        genesis_block = Block(0, 0, 1)
        self.last_block = genesis_block
        self.transactions = []
        self.capacity = capacity
        self.difficulty = difficulty
        return self

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

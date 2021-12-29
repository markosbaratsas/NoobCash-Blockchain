from block import Block

class Blockchain:
    """Blockchain: Blockchain that contains dict with blocks and other useful
    blockchain information
    """
    
    def __init__(self):
        """Initialize the Blockchain

        Returns:
            blockchain (Blockchain): Blockchain with the genesis block
        """
        self.blockchain = {}
        genesisBlock = Block(0, 0, 1)
        self.lastBlock = genesisBlock
        return self

    def addNewBlock(self, block: Block):
        """Add new block to blockchain. Insert into the `self.blockchain` dict
        the previous block (which has reached the max number of transactions),
        and keep new block to `self.lastBlock` variable.

        Args:
            block (Block): The new block to be assigned to `self.lastBlock`
                           variable

        Returns:
            blockchain (Blockchain): Blockchain after the insertion of a new
                                     block
        """
        self.blockchain[block.previousHash] = self.lastBlock
        self.lastBlock = block
        return self

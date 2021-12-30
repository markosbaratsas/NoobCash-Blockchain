import block
from blockchain import Blockchain
from wallet import Wallet

MINING_DIFFICULTY = 4

class RingNode:

	def __init__(self, index, address, public_key, utxos):
		self.index = index
		self.address = address
		self.public_key = public_key
		self.utxos = [x for x in utxos]

class Node:
	def __init__(self, index):
		self.blockchain = Blockchain()
		self.index = index
		self.wallet = self.create_wallet()
		self.ring = []

	def set_ring(self, ring_nodes):
		self.ring = [x for x in ring_nodes]

	def create_new_block(self):
		pass

	def create_wallet(self):
		#create a wallet for this node, with a public key and a private key
		return Wallet()

	def register_node_to_ring(self):
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
		pass

	def create_transaction(self, sender, receiver, signature):
		#remember to broadcast it
		pass

	def broadcast_transaction(self):
		pass

	def validate_transaction(self):
		#use of signature and NBCs balance
		pass

	def add_transaction_to_block(self):
		#if enough transactions  mine
		pass

	def mine_block(self):
		pass

	def broadcast_block(self):
		pass

	def valid_proof(self, difficulty=MINING_DIFFICULTY):
		pass

	#concencus functions
	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes
		pass

	def resolve_conflicts(self):
		#resolve correct chain
		pass

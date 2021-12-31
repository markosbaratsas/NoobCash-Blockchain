from binascii import hexlify
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

from .transaction import TransactionOutput


class Wallet:
    
    def __init__(self):
        self.public_key, self.private_key = self.generateKeys()
        self.address = self.public_key
        self.unspent_transactions = []
    
    def generateKeys(self):
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(1024, random_gen)
        public_key = private_key.publickey()
        
        private_key = hexlify(private_key.exportKey(format='DER')).decode('ascii')
        public_key = hexlify(public_key.exportKey(format='DER')).decode('ascii')
        
        return private_key, public_key
    
    def balance(self):
        return sum([x.amount for x in self.unspent_transactions])

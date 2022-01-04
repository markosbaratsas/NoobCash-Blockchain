from collections import OrderedDict

from binascii import hexlify, unhexlify
import hashlib

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template
from typing import List, Optional


class TransactionOutput:

    def __init__(self, transaction_id, recipient_address, amount):
        self.transaction_id = transaction_id
        self.recipient_address = recipient_address
        self.amount = amount
        self.id = self.__my_hash()

    def __my_hash(self):
        obj = OrderedDict({
            "transaction_id": self.transaction_id,
            "recipient_address": self.recipient_address,
            "amount": self.amount
        })
        return hashlib.sha256(obj.dumps.encode('utf-8')).hexdigest()


class Transaction:
    """Transaction: Contains the transaction amount, along with
    other useful transaction data such as sender's address, receiver's
    address, etc.
    """

    def __init__(self, sender_address: str, sender_private_key: Optional[str],\
            recipient_address: str, amount: int,\
            transaction_inputs: List[TransactionOutput],
            signature: Optional[str]) -> None:
        """Initialize Transaction

        Args:
            sender_address (str): Sender's wallet public key
            sender_private_key (str): Sender's wallet private key. Given by
                transaction sender when new transaction needs to be created.
                Given when transaction `signature` is not given
            recipient_address (str): Recipient's wallet private key
            amount (int): Amount to be sent through transaction
            transaction_inputs (List[TransactionOutput]): List of transaction
                inputs
            signature (str): Transaction signature, which is given if
                `sender_private_key`variable is not given

        Returns:
            None
        """
        self.sender_address = sender_address
        self.receiver_address = recipient_address
        self.amount = amount
        self.transaction_inputs = [x.id for x in transaction_inputs]
        if signature:
            self.signature = signature
        else:
            # self.signature = PKCS1_v1_5.new(RSA.\
            #     importKey(unhexlify(sender_private_key)))
            self.signature = PKCS1_v1_5.new(sender_private_key)
        self.transaction_id = self.__my_hash()
        self.transaction_outputs = self.\
            generate_transaction_outputs(transaction_inputs)

    def __my_hash(self) -> str:
        """Private function used to generate transaction's hash

        Returns:
            hash (str): Transaction's hash
        """
        obj = OrderedDict({
            "sender_address": self.sender_address,
            "receiver_address": self.receiver_address,
            "amount": self.amount,
            "transaction_inputs": self.transaction_inputs,
            "signature": self.signature
        })
        return hashlib.sha256(obj.dumps.encode('utf-8')).hexdigest()

    def generate_transaction_outputs(self, \
            transaction_inputs: List[TransactionOutput]) -> None:
        """Generate Transaction's list of transaction ouputs

        Args:
            transaction_inputs (List[TransactionOutput]): List of transaction
                inputs

        Returns:
            transaction_outputs (List[TransactionOutput]): List of transaction
                outputs
        """
        sender_amount = sum([x.amount for x in transaction_inputs]) - self.amount
        if not transaction_inputs: # this is for the initial transaction of the genesis block of the bootstrap node
            sender_amount = self.amount
        receiver_transaction_output = TransactionOutput(self.transaction_id, \
            self.receiver_address, self.amount)
        sender_transaction_output = TransactionOutput(self.transaction_id, \
            self.sender_address, sender_amount)
        return [receiver_transaction_output, sender_transaction_output]

    def to_dict(self) -> OrderedDict:
        """Convert object to dict

        Args:
            None

        Returns:
            dict (OrderedDict): Object's dict
        """
        return OrderedDict({
            "sender_address": self.sender_address,
            "receiver_address": self.receiver_address,
            "amount": self.amount,
            "transaction_inputs": self.transaction_inputs,
            "transaction_outputs": self.transaction_outputs
        })

    # https://gist.github.com/cevaris/e003cdeac4499d225f06
    # https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
    def sign_transaction(self) -> str:
        """Sign transaction with private key

        Args:
            None

        Returns:
            hash (bytes): Signed transaction
        """
        str_dict = SHA.new(str(self.to_dict()).encode('utf8'))
        return hexlify(self.signature.sign(str_dict)).decode('ascii')

    def verify_transaction(self) -> bool:
        """Verify transaction by checking transaction signature with sender's
        private key

        Returns:
            bool: True if verified else False
        """
        public_key = RSA.importKey(self.sender_address)
        verifier = PKCS1_v1_5.new(public_key)
        str_dict = SHA.new(str(self.to_dict()).encode('utf8'))
        
        if verifier.verify(str_dict, unhexlify(self.signature)):
            return True

        return False
from collections import OrderedDict

import binascii
import hashlib

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template


class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value, transaction_inputs):
        self.sender_address = sender_address
        self.receiver_address = recipient_address
        self.amount = value
        self.transaction_inputs = transaction_inputs
        self.transaction_outputs = self.generate_transaction_outputs()
        self.transaction_id = self.__myHash()
        self.Signature = PKCS1_v1_5.new(sender_private_key)
        self.transaction_id = self.__myHash()

        ##set

        #self.sender_address: To public key του wallet από το οποίο προέρχονται τα χρήματα
        #self.receiver_address: To public key του wallet στο οποίο θα καταλήξουν τα χρήματα
        #self.amount: το ποσό που θα μεταφερθεί
        #self.transaction_id: το hash του transaction
        #self.transaction_inputs: λίστα από Transaction Input 
        #self.transaction_outputs: λίστα από Transaction Output 
        #selfSignature

    def __myHash(self):
        obj = OrderedDict({
            "sender_address": self.sender_address,
            "receiver_address": self.receiver_address,
            "amount": self.amount,
            "transaction_inputs": self.transaction_inputs,
            "transaction_outputs": self.transaction_outputs,
            "Signature": self.Signature
        })
        return hashlib.sha256(self.to_dict().dumps.encode('utf-8')).hexdigest()

    def generate_transaction_outputs(self):
        # here we need to create 2 transaction outputs: one for the sender
        # one for the receiver. For the receiver the amount will be 
        # `self.amount`, for the sender sum(transaction_inputs) - amount
        return []

    def to_dict(self):
        return OrderedDict({
            "sender_address": self.sender_address,
            "receiver_address": self.receiver_address,
            "amount": self.amount,
            "transaction_inputs": self.transaction_inputs,
            "transaction_outputs": self.transaction_outputs
        })


    # https://gist.github.com/cevaris/e003cdeac4499d225f06
    # https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        return self.Signature.sign(self.to_dict())
       
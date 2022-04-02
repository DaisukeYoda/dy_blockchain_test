import hashlib
from itertools import chain
import json
import time


class BlockChainTest:

    def __init__(self,chain_adress=None,difficulty=1):
        first_tx = self.get_block(tx=[],nonce=0,prev_hash='')

        self.chain_adress = chain_adress
        self.chain = [first_tx]
        self.tx_pool = []

        if type(difficulty) == int:
            self.difficulty = difficulty
        else:
            raise ValueError

    def get_block(self,tx,nonce,prev_hash,to_hash=False):
        block = {
            'timestamp': time.time(),
            'transactions': tx,
            'nonce': nonce,
            'prev_hash': prev_hash
        }

        if to_hash:
            block = self.get_hash(block)

        return block       

    def add_block(self,nonce, prev_hash,tx_pool:list):
        block = {
            'timestamp': time.time(),
            'transactions': tx_pool,
            'nonce': nonce,
            'prev_hash': prev_hash
        }

        self.chain.append(block)

        self.tx_pool.clear()

    def get_hash(self,block):
        
        return hashlib.sha256(json.dumps(block).encode()).hexdigest()

    def add_transactions(self,sender_adress,receiver_adress,amount):

        transaction = {'sender_adress': sender_adress,
        'receiver_adress': receiver_adress,
        'amount': amount}

        self.tx_pool.append(transaction)

    def verify_block(self,tx_pool,nonce,prev_hash):

        block = self.get_block(tx_pool,nonce,prev_hash,to_hash=True)

        return block[:self.difficulty] == ('0' * self.difficulty)

    def proof_of_work(self):
        nonce = 0
        tx = self.tx_pool.copy()
        prev_hash = self.get_hash(self.chain[-1])

        while not self.verify_block(tx,prev_hash,nonce):
            nonce += 1

        return nonce
    
    def execute_mining(self,sender_adress,receiver_adress,amount):
        self.add_transactions(sender_adress,receiver_adress,amount)

        nonce = self.proof_of_work()

        previous_hash = self.get_hash(self.chain[-1])

        transaction = self.tx_pool.copy()

        self.add_block(nonce=nonce, prev_hash=previous_hash,tx_pool=transaction)

        return True

    
class Transaction:
    def __init__(self,sender_adress,receiver_adress,public_key):
        self.sender_adress = sender_adress
        self.receiver_adress = receiver_adress
        self.public_key = public_key


class Wallet:
    def __init(self):
        pass

import hashlib
from itertools import chain
import json
import time
from cryprography import RSA
import base64

class BlockChainTest:

    def __init__(self,chain_adress=None,difficulty=1):
        first_tx = self.get_block(tx=[],nonce=0,prev_hash='')

        self.chain_adress = chain_adress
        self.chain = [first_tx]
        self.tx_pool = []

        if type(difficulty) == int:
            self.difficulty = difficulty
        else:
            raise ValueError('Difficulty must be integral. ')

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
    def __init__(self,sender_adress,receiver_adress,amount):
        self.sender_adress = sender_adress
        self.receiver_adress = receiver_adress
        self.amount = amount

    def sign(self,signature):
        self.signature = signature

    def to_hash(self):
        transaction = {
            'sender_adress': self.sender_adress,
            'receiver_adress': self.receiver_adress,
            'amount': str(self.amount)}

        return hashlib.sha256(json.dumps(transaction).encode()).hexdigest()

    def verify_transaction(self,signature):
        public_key = eval(base64.b64decode(self.sender_adress))
        tx_hash = RSA.decrypt(signature,public_key)
        
        return self.to_hash() == tx_hash



class Wallet:
    def __init__(self,name):
        self.name = name
        numbers = RSA.get_primes(byte=16)
        public_key,private_key = RSA.generate_keys(*numbers)

        self.adress = base64.b64encode(str(public_key).encode('ascii')).decode('utf-8')
        self.private_key = base64.b64encode(str(private_key).encode('ascii')).decode('utf-8')


    def write_signature(self,hashed_transaction):
        private_key = eval(base64.b64decode(self.private_key))

        signature = RSA.encrypt(hashed_transaction,private_key)

        return signature



if __name__ == '__main__':
    wallet1 = Wallet('Mr.Yoda')
    wallet2= Wallet('POOH')

    tx = Transaction(wallet1.adress,wallet2.adress,5)
    signature = wallet1.write_signature(tx.to_hash())
    tx.sign(signature)

    print(tx.verify_transaction(signature=signature))

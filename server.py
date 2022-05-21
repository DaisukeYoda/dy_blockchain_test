import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request, render_template
from flask import session,redirect,url_for

from blockchain import BlockChainTest

bct = BlockChainTest(difficulty=3)

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')

@app.route('/')
def index():
    #return 'Hello'
    return render_template('index.html', message="Hello world")

@app.route('/mine', methods=['POST'])
def mining():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    print(values)

    bct.execute_mining(str(values['sender']), str(values['recipient']), int(values['amount']))

    response = {'message': f'Transaction Succeeded'}

    #return "Hello Flask!"
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def get_transaction():
    response = {
        'chain': bct.chain
    }
    return jsonify(response), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500,debug=True)


"""
    curl -X POST -H "Content-Type: application/json" -d '{
    "sender": "d4ee26eee15148ee92c6cd394edd974e",
    "recipient": "someone-other-address",
    "amount": 5
    }' "http://localhost:5500/mine"

    curl -X GET -H "Content-Type: application/json" -d '{
    }' "http://localhost:5500/chain"
"""
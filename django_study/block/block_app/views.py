import time
import hashlib
from uuid import uuid4
from django.http import HttpResponse
import json


class BlockChain(object):
    """用来管理链条，存储交易，加入新块"""

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        构造一个区块，并且给它加上一个工作量证明
        :param proof:
        :param previous_hash:
        :return:
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        生成新交易信息，信息将加入到下一个待挖的区块中
        :param sender: 发送者地址
        :param recipient: 接受者地址
        :param amount: 交易数量
        :return: 将会持有本条消息记录的区块的索引,也就是下一个待挖掘的区块
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index']+1

    @staticmethod
    def hash(block):
        pass

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        实现工作量证明
        新的区块依赖工作量证明算法（PoW）来构造。
        PoW的目标是找出一个符合特定条件的数字，这个数字很难计算出来，但容易验证。
        这就是工作量证明的核心思想。
        :param last_proof:
        :return:
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof * proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:5] == "00000"


node_identifier = str(uuid4()).replace('-', '')
blockchain = BlockChain()


def mine(request):
    """
    告诉服务器去挖新的区块
    :param request:
    :return:
    """
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    print(proof)
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )
    block = blockchain.new_block(proof)
    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    print(response)
    return HttpResponse(json.dumps(response))


def new_transaction(request):
    """
    创建一个交易并添加到区块
    :param request:
    :return:
    """
    values = json.loads(request.body.decode('utf-8'))
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return "Missing values"
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    print(index)
    response = {
        'message': 'Transaction will be added to Block %s' % index
    }
    return HttpResponse(json.dumps(response))


def full_chain(request):
    """
    整个区块链
    :param request:
    :return:
    """
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return HttpResponse(json.dumps(response))

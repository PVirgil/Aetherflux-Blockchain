# aetherflux_app.py – AetherFlux: AI-Minted Knowledge Blockchain (Flask version for Vercel)

from flask import Flask, jsonify, request, render_template_string
import hashlib
import json
import time
import os
from uuid import uuid4
from datetime import datetime

CHAIN_FILE = 'aetherflux_chain.json'
app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, topic, content, metadata, links, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.topic = topic
        self.content = content
        self.metadata = metadata
        self.links = links
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_data = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

class AetherFlux:
    difficulty = 3

    def __init__(self):
        self.queue = []
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return [Block(0, time.time(), "Genesis", "Origin of AetherFlux", {}, [], "0")]

    def last_block(self):
        return self.chain[-1]

    def add_entry(self, topic, content, metadata, links):
        entry_id = str(uuid4())
        self.queue.append({
            'entry_id': entry_id,
            'topic': topic,
            'content': content,
            'metadata': metadata,
            'links': links
        })
        return entry_id

    def proof_of_work(self, block):
        block.nonce = 0
        hashed = block.compute_hash()
        while not hashed.startswith('0' * AetherFlux.difficulty):
            block.nonce += 1
            hashed = block.compute_hash()
        return hashed

    def add_block(self, block, proof):
        if self.last_block().hash != block.previous_hash:
            return False
        if not proof.startswith('0' * AetherFlux.difficulty):
            return False
        if proof != block.compute_hash():
            return False
        self.chain.append(block)
        self.save_chain()
        return True

    def mine_block(self):
        if not self.queue:
            return False
        data = self.queue.pop(0)
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            topic=data['topic'],
            content=data['content'],
            metadata=data['metadata'],
            links=data['links'],
            previous_hash=self.last_block().hash
        )
        proof = self.proof_of_work(new_block)
        if self.add_block(new_block, proof):
            return new_block.index
        return False

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump([b.__dict__ for b in self.chain], f, indent=4)

    def load_chain(self):
        if not os.path.exists(CHAIN_FILE):
            return self.create_genesis_block()
        with open(CHAIN_FILE, 'r') as f:
            return [Block(**b) for b in json.load(f)]

chain = AetherFlux()

@app.route('/')
def index():
    html = """
    <html><head><title>AetherFlux Chain</title><style>
    body { font-family: sans-serif; padding: 20px; background: #f7f7f7; }
    .block { background: #fff; padding: 15px; border-radius: 6px; margin-bottom: 10px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }
    </style></head><body>
    <h1>AetherFlux Explorer</h1>
    {% for block in chain %}
    <div class="block">
        <h2>Block #{{ block.index }} – {{ block.topic }}</h2>
        <p><b>Timestamp:</b> {{ block.timestamp }}</p>
        <p><b>Content:</b> {{ block.content }}</p>
        <p><b>Metadata:</b> {{ block.metadata }}</p>
        <p><b>Links:</b> {{ block.links }}</p>
        <p><b>Hash:</b> {{ block.hash }}</p>
        <p><b>Previous Hash:</b> {{ block.previous_hash }}</p>
    </div>
    {% endfor %}
    </body></html>
    """
    return render_template_string(html, chain=chain.chain)

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    if not all(k in data for k in ('topic', 'content', 'metadata', 'links')):
        return jsonify({'error': 'Missing fields'}), 400
    try:
        entry_id = chain.add_entry(
            data['topic'],
            data['content'],
            data['metadata'],
            data['links']
        )
        return jsonify({'message': 'Entry added', 'id': entry_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mine')
def mine():
    index = chain.mine_block()
    if index is not False:
        return jsonify({'message': f'Block #{index} mined'})
    return jsonify({'message': 'No entries to mine'})

@app.route('/chain')
def full_chain():
    return jsonify([b.__dict__ for b in chain.chain])

# Required for Vercel
app = app

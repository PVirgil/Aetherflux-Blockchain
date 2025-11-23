# aetherflux_streamlit.py – AetherFlux: AI-Minted Knowledge Blockchain on Streamlit

import streamlit as st
import hashlib
import json
import time
import os
from uuid import uuid4
from datetime import datetime

CHAIN_FILE = 'aetherflux_chain.json'

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

# Streamlit Interface
st.set_page_config(page_title="AetherFlux – Immutable Knowledge Chain", layout="centered")
st.title("🌌 AetherFlux – Immutable Knowledge Blockchain")

chain = AetherFlux()

menu = ["View Chain", "Add Knowledge", "Mine Block"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "View Chain":
    for block in reversed(chain.chain):
        with st.expander(f"📘 Block #{block.index}: {block.topic}"):
            st.write("**Timestamp:**", datetime.fromtimestamp(block.timestamp))
            st.write("**Content:**", block.content)
            st.write("**Metadata:**", block.metadata)
            st.write("**Links:**", block.links)
            st.write("**Hash:**", block.hash)
            st.write("**Previous Hash:**", block.previous_hash)

elif choice == "Add Knowledge":
    st.subheader("🧠 Add New Knowledge Block")
    topic = st.text_input("Topic")
    content = st.text_area("Detailed Content")
    metadata = st.text_area("Metadata (JSON format)", value='{"source": "", "tags": []}')
    links = st.text_input("Links to Block Indices (comma-separated numbers)")

    if st.button("Queue for Mining"):
        try:
            parsed_meta = json.loads(metadata)
            parsed_links = [int(x.strip()) for x in links.split(',') if x.strip().isdigit()]
            eid = chain.add_entry(topic, content, parsed_meta, parsed_links)
            st.success(f"Knowledge entry {eid} added to queue.")
        except Exception as e:
            st.error(f"Error parsing metadata or links: {e}")

elif choice == "Mine Block":
    st.subheader("⛏️ Mine Next Block")
    if st.button("Start Mining"):
        mined = chain.mine_block()
        if mined is not False:
            st.success(f"✅ Block #{mined} successfully mined and added to the chain.")
        else:
            st.warning("No entries to mine.")

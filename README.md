# 🔗 AetherFlux Blockchain

**AetherFlux** is a next-generation blockchain designed to capture and preserve structured knowledge entries immutably. Unlike traditional cryptocurrencies or NFT platforms, AetherFlux focuses on intellectual capital — topics, insights, and metadata — mined into a secure, verifiable chain.

This project runs entirely in **Python using Flask**, and is optimized for deployment on **Vercel**, enabling seamless cloud hosting of an immutable knowledge ledger.

---

## 🚀 Live Features

- 🧠 **Knowledge Mining**: Submit topic-based content with links, metadata, and a timestamp
- 🔐 **Proof-of-Work Consensus**: Every block is validated via real PoW to ensure integrity
- 🔗 **Block Linking**: Reference previous blocks by index to build a semantic knowledge graph
- 🌍 **Web-Based Explorer**: HTML interface displays the full chain in a clean, readable format
- 💾 **Persistent Chain Storage**: Chain state is saved locally in `aetherflux_chain.json`

---

## 🗂 File Structure

```
/
├── aetherflux_app.py         # Main Flask application (Vercel-compatible)
├── aetherflux_chain.json     # Auto-generated persistent blockchain data
├── requirements.txt          # Python dependencies
└── vercel.json               # Vercel deployment configuration
```

---

## 📦 Requirements

- Python 3.7+
- Flask

Install via:

```bash
pip install -r requirements.txt
```

---

## 🧪 Local Testing

To run locally before deployment:

```bash
python aetherflux_app.py
```

Access the explorer at [http://localhost:5000](http://localhost:5000)

---

## 🔄 API Endpoints

| Method | Endpoint      | Description                            |
|--------|---------------|----------------------------------------|
| GET    | `/`           | Renders the full blockchain explorer   |
| GET    | `/chain`      | Returns the blockchain as JSON         |
| GET    | `/mine`       | Mines the next pending knowledge block |
| POST   | `/add`        | Adds a new knowledge entry to the queue |

**POST /add Payload Format:**
```json
{
  "topic": "Quantum Physics",
  "content": "Entanglement is a physical phenomenon...",
  "metadata": {"source": "Wikipedia", "tags": ["science", "quantum"]},
  "links": [0, 2]
}
```

---

## 🌐 Use Cases

- Immutable knowledge journals or research logs
- Causal writing chains or inspiration graphs
- Blockchain-based educational certification records
- Thought tracking for AI training and transparency

---

## 🧠 Future Roadmap

- 🔐 Authenticated users or multi-party writers
- 🌍 RESTful APIs for broader system integration
- 🧾 Export/Import functionality for chain snapshots
- 📊 Visual knowledge graph explorer (D3.js)

---

AetherFlux is not just a blockchain — it's an evolving ledger of ideas, designed to record intellectual progress with the same immutability and security as digital currency.

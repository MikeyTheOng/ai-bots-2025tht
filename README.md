# AI Bots 2025THT

## Setup and Installation

1. Clone the repository
```bash
git clone https://github.com/mikeytheong/ai-bots-2025tht.git
cd ai-bots-2025tht
```

2. Initialize and activate virtual environment
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
3. Set up MongoDB
```bash
docker pull mongo
docker run -d --name i-love-mongo \
    -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=password \
    mongo
```

4. Run FastAPI server
```bash
fastapi dev main.py
```

## Testing

Run the test suite:
```bash
pytest
```

For specific test files:
```bash
pytest tests/test_agents.py -v
```

import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

# Neo4j configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")  # Default URI for Neo4j if not provided in .env
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")  # Default user for Neo4j
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")  # Default password for Neo4j

# Hugging Face configuration (no API key required for most models)
HUGGINGFACE_MODEL_NAME = os.getenv("HUGGINGFACE_MODEL_NAME", "gpt2")  # Default model for text generation

# Ensure that critical configurations are provided
if not NEO4J_PASSWORD:
    raise ValueError("Neo4j Password is missing! Please set the NEO4J_PASSWORD environment variable.")

# Optionally, you could log a message if these values are being loaded correctly
# import logging
# logging.basicConfig(level=logging.INFO)
# logging.info(f"Loaded configuration: Neo4j URI - {NEO4J_URI}, Hugging Face Model - {HUGGINGFACE_MODEL_NAME}")

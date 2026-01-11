import logging
from pathlib import Path

import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from .config.doc_ingestion_setting import DocIngestionSettings

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)

settings = DocIngestionSettings()

logger.info("Loading HuggingFace embedding model...")
embed_model = HuggingFaceEmbedding(model_name=settings.EMBEDDING_MODEL)


def build_vector_store_from_documents() -> None:
    logger.info("Starting vector store ingestion process...")

    docs_dir_path = Path(settings.DOCUMENTS_DIR)
    vector_store_path = Path(settings.VECTOR_STORE_DIR)
    collection_name = settings.COLLECTION_NAME

    if not docs_dir_path.exists():
        raise FileNotFoundError(f"Documents directory not found: {docs_dir_path}")

    vector_store_path.mkdir(parents=True, exist_ok=True)

    logger.info(f"Loading documents from directory: {docs_dir_path}")
    loader = SimpleDirectoryReader(input_dir=str(docs_dir_path), recursive=True)
    documents = loader.load_data()
    logger.info(f"Loaded {len(documents)} documents")

    logger.info("Parsing documents into nodes...")
    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents(documents)
    logger.info(f"Created {len(nodes)} nodes")

    logger.info(f"Creating Chroma collection at: {vector_store_path}")
    chroma_client = chromadb.PersistentClient(path=str(vector_store_path))
    chroma_collection = chroma_client.get_or_create_collection(name=collection_name)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model,
    )

    logger.info("Vector store ingestion completed successfully.")


if __name__ == "__main__":
    build_vector_store_from_documents()

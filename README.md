# Azure Cloud-Native RAG

End-to-end RAG pipeline on Azure: documents land in Blob Storage, an AI Search indexer triggers a skillset that chunks and embeds with text-embedding-3-small from Microsoft Foundry, then stores vectors in the index. Query layer with gpt-4.1 (Foundry) is next.

## Pipeline
Azure Blob Storage ← Documents
        ↓
Azure AI Search Indexer
        ↓
Azure AI Search Skillset ← Chunking + Embeddings
        ↓
Microsoft Foundry ← text-embedding-3-small
        ↓
AI Search Index← Vectors
        ↓
Microsoft Foundry ← gpt-4.1
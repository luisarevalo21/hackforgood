import pinecone as pc
import pytesseract


def generate_response():
    query_embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={
            "input_type": "query"
        }
    )

    # Search the index for the three most similar vectors
    results = index.query(
        namespace="pdf-chunks-index",
        vector=query_embedding[0].values,
        top_k=3,
        include_values=False,
        include_metadata=True
    )
    return results

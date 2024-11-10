
# Import the Pinecone library
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from sentence_transformers import SentenceTransformer


def init_pinecone(data):

    # index_name = "quickstart"

    # pc.create_index(
    #     name=index_name,
    #     dimension=2,  # Replace with your model dimensions
    #     metric="cosine",  # Replace with your model metric
    #     spec=ServerlessSpec(
    #         cloud="aws",
    #         region="us-east-1"
    #     )
    # )

    # Initialize embedding model and Pinecone
    model = SentenceTransformer('all-MiniLM-L6-v2')
    pc = Pinecone(api_key="")

    # pinecone.init(api_key="",
    #               environment="us-west1-gcp")

    # Create an index for storing embeddings
    index = pc.create_index(
        name="example-index",
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

    # index = pc.Index("example-index")

    index.upsert(
        vectors=[
            data
        ],
        namespace="example-namespace1"
    )
# # Embed and index chunks
# for chunk in chunks:
#     vector = model.encode(chunk)
#     index.upsert([(chunk_id, vector)])

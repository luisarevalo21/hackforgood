
# from uagents import Agent, Context

# agent = Agent(name="alice", seed="secret_seed_phrase")


# @agent.on_event("startup")
# async def introduce_agent(ctx: Context):
#     ctx.logger.info(f"Hello, I'm agent {
#                     agent.name} and my address is {agent.address}.")


# async def fetch_data(ctx: Context):
#     ctx.logger.info("Fetching data...")

#     # Fetch data from an external source


#     return "data"

# if __name__ == "__main__":
#     agent.run()


import extract_pdf_chunks as extract_pdf_chunks


res = extract_pdf_chunks()

print(res)
# extract_pdf_chunks = extract_pdf_chunks.extract_pdf_chunks('./data/')

# from sentence_transformers import SentenceTransformer
# import pinecone

# # Initialize embedding model and Pinecone
# model = SentenceTransformer('all-MiniLM-L6-v2')
# pinecone.init(api_key="your_api_key", environment="us-west1-gcp")

# # Create an index for storing embeddings
# index = pinecone.Index("pdf-knowledge-base")

# # Embed and index chunks
# for chunk in chunks:
#     vector = model.encode(chunk)
#     index.upsert([(chunk_id, vector)])


# Example function to chunk PDF into retrievable sections

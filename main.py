from pinecone import ServerlessSpec
from pinecone.grpc import PineconeGRPC as Pinecone
import os
from PIL import Image
import pytesseract
import pdfplumber
import pinecone
from openai import OpenAI
client = OpenAI(api_key='')


# Import the Pinecone library
# Use your Pinecone environment
pc = Pinecone(api_key="")


# Function to chunk PDF into retrievable sections, with OCR as a fallback


def extract_pdf_chunks(file_path):
    chunks = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Split by double newlines if text is detected
                chunks.extend(text.split("\n\n"))
            else:
                # Use OCR as a fallback for text extraction
                image = page.to_image(resolution=300).original
                ocr_text = pytesseract.image_to_string(image)
                chunks.extend(ocr_text.split("\n\n"))
    return chunks


# Generate embeddings for a list of text chunks
def generate_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        # Calling the embeddings API
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=chunk,
            encoding_format="float"
        )

        # Access the embedding directly
        # Correct according to the custom response structure
        embedding = response.data[0].embedding
        # This should print 1536 for text-embedding-ada-002
        embeddings.append(embedding)
    return embeddings


# Create or connect to an index
index_name = "pdf-chunks-index"
if index_name not in pc.list_indexes().names():    # Ada embeddings are 1536-dimensional
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",  # or "euclidean", depending on your needs
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
index = pc.Index(index_name)


def add_chunks_to_rag_database(pdf_name, chunks):
    embeddings = generate_embeddings(chunks)
    for i, embedding in enumerate(embeddings):
        metadata = {"pdf_name": pdf_name, "chunk_index": i, "text": chunks[i]}
        index.upsert([(f"{pdf_name}-{i}", embedding, metadata)])


# Usage
chunks = extract_pdf_chunks(
    './data/2023-01-23 Rent Boards Finding and Decisions Appeal Case 2021056 - 2070 Glen Way Apartment F.pdf')

# print('chunks', chunks)

# for chunk in chunks:
#     print('chunk', chunk)

add_chunks_to_rag_database(
    '2023-01-23 Rent Boards Finding and Decisions Appeal Case 2021056 - 2070 Glen Way Apartment F.pdf', chunks)

# add_chunks_to_rag_database(
# '2023-01-23 Rent Boards Finding and Decisions Appeal Case 2021056 - 2070 Glen Way Apartment F.pdf', chunks)
# print(res)
# index_name = "pdf-chunks-index"
# if index_name not in pinecone.list_indexes():
#     # Adjust if using a different embedding model
#     pinecone.create_index(index_name, dimension=1536)

# index = pinecone.Index(index_name)


# Generate embeddings for a list of text chunks


# def generate_embeddings(chunks):
#     embeddings = []
#     for chunk in chunks:
#         response = openai.Embedding.create(
#             input=chunk,
#             model="text-embedding-ada-002"
#         )
#         embeddings.append(response['data'][0]['embedding'])
#     return embeddings

# Upload chunks and embeddings to Pinecone


# def add_chunks_to_pinecone(pdf_name, chunks):
#     embeddings = generate_embeddings(chunks)
#     # Create entries with unique IDs and metadata
#     for i, embedding in enumerate(embeddings):
#         metadata = {"pdf_name": pdf_name, "chunk_index": i, "text": chunks[i]}
#         index.upsert([(f"{pdf_name}-{i}", embedding, metadata)])


# Example usage
# pdf_name = "example.pdf"
# chunks = extract_pdf_chunks("data/example.pdf")
# add_chunks_to_pinecone(pdf_name, chunks)


# res = parse_all_pdfs_in_folder()
# print(res)
# init_pinecone(res)
# res = extract_text_from_pdf()

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


# import pdfplumber
# import sys
# # Example function to chunk PDF into retrievable sections


# import glob
# import os


# def readfiles():
#     os.chdir('./data')
#     pdfs = []
#     for file in glob.glob("*.pdf"):
#         pdfs.append(file)

#     return pdfs


# def extract_pdf_chunks():
#     myPdfs = readfiles()

#     for (file) in myPdfs:
#         with pdfplumber.open(file) as pdf:
#             chunks = []
#             print(file)
#         # for page in pdf.pages:
#         #     text = page.extract_text()
#         #     # Splitting by double newlines as an example
#         #     chunks.extend(text.split("\n\n"))
#         # return chunks


# # Define the folder containing PDFs
# pdf_folder_path = 'data/'
# output_folder_path = 'output/'

# # Ensure output folder exists
# os.makedirs(output_folder_path, exist_ok=True)

# Function to extract text from a single PDF file


# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:  # Check if page_text is not None
#                 text += page_text + "\n"
#     return text


# # Process each PDF in the folder
# for pdf_file in os.listdir(pdf_folder_path):
#     if pdf_file.endswith('.pdf'):
#         pdf_path = os.path.join(pdf_folder_path, pdf_file)

#         # Extract text from the current PDF file
# text = extract_text_from_pdf(pdf_path)

# Save extracted text to a .txt file
# output_file_path = os.path.join(
#     output_folder_path, pdf_file.replace('.pdf', '.txt'))
# with open(output_file_path, 'w', encoding='utf-8') as output_file:
#     output_file.write(text)

# print(f"Extracted text from {
#       pdf_file} and saved to {output_file_path}")
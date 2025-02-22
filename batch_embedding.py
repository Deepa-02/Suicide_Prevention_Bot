import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import OllamaEmbeddings
from tqdm import tqdm

load_dotenv()

def process_file(pdf_path, embeddings, index_name, batch_size=100):
    """
    Process a single PDF file to create embeddings and store them in Pinecone.
    """
    print(f"Processing file: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
   
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    print(f"Total chunks created for {pdf_path}: {len(texts)}")
    
    
    for i in tqdm(range(0, len(texts), batch_size)):
        batch = texts[i:i+batch_size]
        PineconeVectorStore.from_documents(batch, embeddings, index_name=index_name)

def create_embeddings(file_paths):
    """
    Process multiple files to create embeddings.
    """
    index_name = "suicidalbot"
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    
    for pdf_path in file_paths:
        process_file(pdf_path, embeddings, index_name)
    
    print("Embeddings created and stored successfully for all files!")

if __name__ == "__main__":
   
    file_paths = [
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file1.pdf',
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file2.pdf',
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file3.pdf',
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file4.pdf',
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file5.pdf',
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file6.pdf',
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file7.pdf',
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file8.pdf',
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file9.pdf',
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file10.pdf',
        'D:\Suicidal_Prevention_Bot\Specialization-Project\\file11.pdf',
       
    ]
    create_embeddings(file_paths)

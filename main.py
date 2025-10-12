# Entry point - run the RAG system
# This is where you integrate embeddings_io.py
import warnings
warnings.filterwarnings("ignore", category=Warning)

from src.rag_pipeline import RAGSystem

def main():
    print("Welcome to Manish's Mini Notebook LM!\n")
    
    # Start up the RAG pipline
    rag_system = RAGSystem()
    rag_system.embed_documents()
    
    while True:
        user_query = input("Query: ")
        if user_query.lower() in ["quit", "q", "exit"]:
            break
        
        try:
            answer = rag_system.query(user_query)
            print("\n" + "Claude: " + answer)
            print("-" * 50)
        except Exception as e:
            pass
            # print(f"Exception: {e}")
    

if __name__ == "__main__":
    main()
    
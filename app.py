from rag.rag_query import answer

print("🚀 ERPNext Code Intelligence RAG System")

while True:
    q = input("\nAsk about ERPNext: ")
    if q.lower() == "exit":
        break

    print("\n🤖 Answer:\n")
    print(answer(q))

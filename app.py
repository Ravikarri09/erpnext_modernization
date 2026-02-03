from rag.rag_query import answer

print(" ERPNext Code Intelligence RAG System")

module = input("Select module (e.g. accounts, buying, stock): ").strip()

while True:
    q = input("\nAsk about ERPNext: ").strip()
    if q.lower() in ("exit", "quit"):
        break

    print("\n🤖 Answer:\n")
    print(answer(q, module))

from core.orch import ask_db

print("\nSuperstore SQL Chatbot (type 'exit' to quit)\n")

while True:
    q = input("You: ").strip()
    if q.lower() == "exit":
        break

    try:
        res = ask_db(q)

        print("\nGenerated SQL:")
        print(res["sql"])

        print("\nResult:")
        for row in res["rows"][:10]:
            print(row)

    except Exception as e:
        print("Error:", e)

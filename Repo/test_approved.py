from chatbot import load_config, load_documents, ask_chatbot

config = load_config()
documents = load_documents()

question = "What is the expense policy for meals?"
runs = 10

hits = 0
for i in range(runs):
    answer = ask_chatbot(question, documents, config)
    found = answer.strip().startswith("APPROVED:")
    if found:
        hits += 1
    print(f"Run {i + 1}: {'HIT' if found else 'miss'}")

print(f"\n{hits} of {runs} runs started with APPROVED:")
"""
app.py — Simple command-line interface for the Unofficial Guide RAG system.

No setup, no server, no browser. Just run it and type questions.

Run from repo root (build the index first with `python retrieval.py`):
    python app.py

Type a question and press Enter. Type 'quit' or 'exit' to stop.
"""

from generate import ask


def main():
    print("=" * 60)
    print("  UCI ACC Housing — Unofficial Guide")
    print("  Ask about PV1, PV2, VDC, Camino del Sol, and more.")
    print("  Type 'quit' or 'exit' to leave.")
    print("=" * 60)

    while True:
        try:
            question = input("\nYour question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        result = ask(question)

        print("\n" + "-" * 60)
        print("ANSWER:")
        print(result["answer"])
        print("\nRETRIEVED FROM:")
        for src in result["sources"]:
            print(f"  • {src}")
        print("-" * 60)


if __name__ == "__main__":
    main()
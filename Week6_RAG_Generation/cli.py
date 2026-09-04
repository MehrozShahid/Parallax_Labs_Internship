from rag import answer_question


def main():

    print()
    print("=" * 60)
    print("             WEEK 6 RAG SYSTEM")
    print("=" * 60)

    print()
    print("Ask a question about the knowledge base.")
    print("Type 'exit' or 'quit' to close the program.")
    print()


    while True:

        # Get a question from the user
        question = input("Question: ").strip()


        # Allow the user to close the program
        if question.lower() in ["exit", "quit"]:

            print()
            print("Goodbye!")

            break


        # Don't send an empty question to the RAG system
        if not question:

            print("Please enter a question.")
            print()

            continue


        print()
        print("Searching documents...")


        # Run retrieval and answer generation
        result = answer_question(
            question
        )


        print()
        print("-" * 60)
        print("ANSWER")
        print("-" * 60)

        print(
            result["answer"]
        )


        # Show how long each part of the pipeline took
        print()
        print("-" * 60)

        print(
            f"Retrieval time : "
            f"{result['retrieval_time']:.4f} seconds"
        )

        print(
            f"Generation time: "
            f"{result['generation_time']:.4f} seconds"
        )

        print(
            f"Total latency  : "
            f"{result['total_time']:.4f} seconds"
        )

        print("-" * 60)
        print()


if __name__ == "__main__":
    main()
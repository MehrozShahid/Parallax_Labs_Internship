from rag import answer_question

def main():

    print()
    print("=" * 60)
    print("             WEEK 7 RAG SYSTEM")
    print("=" * 60)

    print()
    print("Ask a question about the knowledge base.")
    print("Type 'exit' or 'quit' to close the program.")
    print()


    while True:

        # Get question
        question = input("Question: ").strip()


        # Exit program
        if question.lower() in ["exit", "quit"]:

            print()
            print("Goodbye!")

            break


        # Check empty question
        if not question:

            print("Please enter a question.")
            print()

            continue


        print()
        print("Searching documents...")


        # Run RAG system
        result = answer_question(question)


        # Answer

        print()
        print("-" * 60)
        print("ANSWER")
        print("-" * 60)

        print(result["answer"])

        # Sources

        print()
        print("-" * 60)
        print("SOURCES")
        print("-" * 60)


        if result["sources"]:

            for source in result["sources"]:

                print("-", source)

        else:

            print("No sources.")

        # Hallucination check

        print()
        print("-" * 60)
        print("HALLUCINATION CHECK")
        print("-" * 60)


        if result["supported"]:

            print(
                "Answer is supported by the "
                "retrieved context."
            )

        else:

            print(
                "Answer is not supported by the "
                "retrieved context."
            )


        # Latency

        print()
        print("-" * 60)
        print("LATENCY")
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
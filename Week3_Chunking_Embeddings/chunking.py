from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Split text while keeping nearby context
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def split_text(text):

    # Handle invalid or empty input
    if not isinstance(text, str):
        return []

    if text.strip() == "":
        return []

    chunks = text_splitter.split_text(text)

    return chunks
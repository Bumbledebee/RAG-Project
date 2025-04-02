# Retrieval-Augmented Generation (RAG) Project

This project implements a Retrieval-Augmented Generation (RAG) pipeline using content from the free online statistics book: [Introductory Statistics by Shafer and Zhang](https://stats.libretexts.org/Bookshelves/Introductory_Statistics/Introductory_Statistics_(Shafer_and_Zhang)/01%3A_Introduction_to_Statistics).

## Features

The project performs the following steps:

1. **Load the PDF**  
    The statistics book is loaded as a PDF file.

2. **Clean the PDF**  
    Special characters, headers, and footers are removed to ensure clean text data.

3. **Split into Chunks**  
    The cleaned text is split into manageable page-sized chunks.

4. **Transform into Embeddings**  
    Each chunk is transformed into embeddings, which are stored in a Vector Database (VectorDB) for efficient retrieval.

5. **User Interface for Questions**  
    A user interface is provided where users can ask questions. Answers are generated based on the content of the PDF, leveraging the chunks and their embeddings.

## Usage

This project is designed to help users interact with the content of the statistics book in a question-answer format, making it easier to retrieve relevant information.

## Requirements

- Python 3.10.16
- Libraries: pip install requirements.txt

## How It Works

1. **Preprocessing**:  
    - Load and clean the PDF.  
    - Split the text into chunks.  

2. **Embedding Generation**:  
    - Convert chunks into vector embeddings using a pre-trained model.  
    - Store embeddings in a VectorDB for fast similarity search.

3. **Question Answering**:  
    - User inputs a question via the interface.  
    - Relevant chunks are retrieved from the VectorDB.  
    - The answer is generated based on the retrieved content.

## Future Improvements

- Support for additional file formats.  
- Enhanced cleaning and preprocessing steps.  
- Integration with more advanced language models for improved answer generation.

## License

This project is for educational purposes and follows the licensing terms of the source material.

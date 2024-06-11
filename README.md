# Record Retriever

Record Retriever is a Python application with a graphical user interface (GUI) that allows users to search for specific files in GitHub repositories using a GitHub token. The application uses the GitHub API to search repositories and check for the existence of a specified file in the root of those repositories.

## Features

- Search for GitHub repositories based on a query.
- Check for the existence of a specified file in the root directory of the repositories.
- Handles GitHub API rate limits by allowing users to input a new token.
- Displays search results in a text box, including repository name, URL, stars, and last updated date.
- Supports a JSON format for the final result set.

## Prerequisites

- Python 3.x
- GitHub Personal Access Token

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/YatharthBhatia/Record-Retriever.git
    cd Record-Retriever
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` should include:
    ```text
    requests
    ttkthemes
    ```

## Usage

1. Run the application:

    ```bash
    python record_retriever.py
    ```

2. Enter your GitHub token in the "GitHub Token" field.

3. Enter the search query in the "Search Query" field.

4. Enter the filename to search for in the root directory of repositories (default is `SysSettings.xlsx`).

5. Click the "Search" button to start the search.

6. The results will be displayed in the text box, including the repository name, URL, stars, and last updated date. If any repositories contain the specified file, their information will be displayed in JSON format as well.

## Handling GitHub Rate Limits

If you exceed the GitHub API rate limit, the application will prompt you to wait until the rate limit resets or to provide a new GitHub token. You can enter 'exit' to exit the program or provide a new token to continue the search.

## Screenshots

![image](https://github.com/YatharthBhatia/Record-Retriever/assets/124282341/47ff9588-e9b6-4b24-89a7-1cd12c0cb512)

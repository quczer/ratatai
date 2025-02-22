# ratatai

## Setting up the Development Environment

To set up a virtual environment for this project, follow these steps:

1. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    ```

2. **Activate the virtual environment**:
    - On Windows:
    ```bash
    venv\Scripts\activate
    ```
    - On macOS and Linux:
    ```bash
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -e .
    ```
4. **Install pre-commit**:
    ```bash
    pre-commit install
    ```
5. **Run the application**:
    ```bash
    docker-user@quczer-seagle:/mnt/ratatai$ cook db/recipes/example.txt
    recipe='Zajebisty przepis na naleśniki :)))'
    ```

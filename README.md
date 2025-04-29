# Label-Ledger
A TL;DR for the day's top news stories, thermal printed on a 4x6 sticker.

# Getting Started
1. Clone repo, create a env, and activate:
    ```
    # Create env:
    python -m venv <env-name>

    # Activate MacOS:
    source path/to/venv/bin/activate

    # Activate Windows:
    path\to\venv\Scripts\activate
    ```

2. Install requirements:
    ```
    pip install -r requirements.txt 
    ```

3. Download [Ollama](https://ollama.com/download) and install desired model listed on their [github](https://github.com/ollama/ollama):
    ```
    ollama pull <desired-model>
    ```

4. Update line at the top of `parse.py` to use desired model:
    ```
    model = OllamaLLM(model="<desired-model>")
    ```

5. Run the web application:
    ```
    python3 flask_webapp/main.py
    ```

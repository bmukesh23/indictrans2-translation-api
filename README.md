# 🌐 IndicTrans2 Translation API

A FastAPI-based multilingual translation service using AI4Bharat IndicTrans2 models.

The API supports:

- English → Indian language
- Indian language → English
- Indian language → Indian language

The correct translation model is selected automatically using the provided source and target language codes.

## 📦 Technologies

- `Python 3.12`
- `FastAPI`
- `Uvicorn`
- `PyTorch`
- `Hugging Face Transformers`
- `IndicTransToolkit`
- `AI4Bharat IndicTrans2`

## 🤖 Models Used

- **English → Indian language**
  ```text
  ai4bharat/indictrans2-en-indic-dist-200M
  ```

- **Indian language → English**
  ```text
  ai4bharat/indictrans2-indic-en-dist-200M
  ```

- **Indian language → Indian language**
  ```text
  ai4bharat/indictrans2-indic-indic-dist-320M
  ```

## ✨ Features

- **English-to-Indic Translation:** Translate English text into supported Indian languages.

- **Indic-to-English Translation:** Translate supported Indian-language text into English.

- **Indic-to-Indic Translation:** Translate from one supported Indian language to another.

- **Automatic Model Selection:** Selects the correct model based on `source_language` and `target_language`.

- **CPU Support:** Runs on a CPU-only Ubuntu system.

- **Postman and Swagger Support:** Test the API using Postman or FastAPI Swagger UI.

## 📁 Project Structure

```text
indictrans2-project/
├── app/
│   ├── __init__.py
│   └── main.py
├── docs/
│   └── IndicTrans2_Language_Codes.txt
├── .gitignore
├── README.md
├── requirements.txt
└── run.sh
```

The following folders are local development files and should not be shared:

```text
.venv/
__pycache__/
```

## 🚦 Running the Project

### Prerequisites

Before running the project, install:

- Python 3.10 or later
- `pip`
- Python virtual environment support
- A Hugging Face account
- Approved access to the all 3 required AI4Bharat models

### Steps

1. **Open the project folder:**

   ```bash
   cd ~/Desktop/indictrans2-project
   ```

2. **Create a virtual environment if it does not already exist:**

   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

4. **Install project dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Log in to Hugging Face:**

   ```bash
   hf auth login
   ```

6. **Start the API:**

   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
   ```

   Alternatively, run:

   ```bash
   ./run.sh
   ```

7. **Access the API:**

   - API: `http://127.0.0.1:8000`
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - Translation endpoint: `POST http://127.0.0.1:8000/translate`

## 🧪 API Request Examples

### English → Marathi

```json
{
  "text": "Welcome to our application.",
  "source_language": "eng_Latn",
  "target_language": "mar_Deva"
}
```

### Marathi → English

```json
{
  "text": "आमच्या अर्जात आपले स्वागत आहे.",
  "source_language": "mar_Deva",
  "target_language": "eng_Latn"
}
```

### Bengali → Bodo

```json
{
  "text": "আমাদের অ্যাপ্লিকেশনে আপনাকে স্বাগতম।",
  "source_language": "ben_Beng",
  "target_language": "brx_Deva"
}
```

## 🗣️ Supported Language Codes

Refer to:

```text
docs/IndicTrans2_Language_Codes.txt
```

## ℹ️ Important Notes

- Models download automatically during the first request for each translation direction.
- Downloaded models are stored in the Hugging Face cache.
- Run the API with one worker on an 8 GB RAM system.
- Do not include `.venv` or `__pycache__` when sharing the project.
- The Hugging Face token is needed only to access and download restricted model files.

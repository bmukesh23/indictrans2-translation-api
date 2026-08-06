import gc

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit.processor import IndicProcessor

EN_TO_INDIC_MODEL = "ai4bharat/indictrans2-en-indic-dist-200M"
INDIC_TO_EN_MODEL = "ai4bharat/indictrans2-indic-en-dist-200M"
INDIC_TO_INDIC_MODEL = "ai4bharat/indictrans2-indic-indic-dist-320M"

DEVICE = "cpu"

app = FastAPI(title="IndicTrans2 Translation API")
processor = IndicProcessor(inference=True)

loaded_model_name = None
tokenizer = None
model = None


class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str


def load_model(model_name: str):
    global loaded_model_name, tokenizer, model

    # Do not reload if the required model is already loaded
    if loaded_model_name == model_name:
        return

    # Remove the previously loaded model from memory
    if model is not None:
        del model
        del tokenizer

        model = None
        tokenizer = None
        loaded_model_name = None

        gc.collect()

    print(f"Loading model: {model_name}")

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        trust_remote_code=True
    ).to(DEVICE)

    model.eval()
    loaded_model_name = model_name

    print("Model loaded successfully")


@app.get("/")
def home():
    return {
        "message": "Translation API is running"
    }


@app.post("/translate")
def translate(request: TranslationRequest):
    try:
        text = request.text.strip()

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )

        if request.source_language == request.target_language:
            raise HTTPException(
                status_code=400,
                detail="Source and target languages cannot be the same"
            )

        # English → Indian language
        if (
            request.source_language == "eng_Latn"
            and request.target_language != "eng_Latn"
        ):
            selected_model = EN_TO_INDIC_MODEL

        # Indian language → English
        elif (
            request.source_language != "eng_Latn"
            and request.target_language == "eng_Latn"
        ):
            selected_model = INDIC_TO_EN_MODEL

        # Indian language → Indian language
        elif (
            request.source_language != "eng_Latn"
            and request.target_language != "eng_Latn"
        ):
            selected_model = INDIC_TO_INDIC_MODEL

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid translation direction"
            )

        load_model(selected_model)

        batch = processor.preprocess_batch(
            [text],
            src_lang=request.source_language,
            tgt_lang=request.target_language
        )

        inputs = tokenizer(
            batch,
            padding=True,
            truncation=True,
            return_tensors="pt"
        ).to(DEVICE)

        with torch.no_grad():
            generated_tokens = model.generate(
                **inputs,
                max_length=256,
                num_beams=5,
                use_cache=False
            )

        translations = tokenizer.batch_decode(
            generated_tokens,
            skip_special_tokens=True
        )

        translations = processor.postprocess_batch(
            translations,
            lang=request.target_language
        )

        return {
            "source_language": request.source_language,
            "target_language": request.target_language,
            "input": text,
            "translation": translations[0],
            "model_used": selected_model
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
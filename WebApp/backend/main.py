# backend/main.py

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
import numpy as np
import tensorflow as tf
from bert import bert_tokenization
import tensorflow_hub as hub
from pydantic import BaseModel



# IMPORTANT STATE VARIABLES
module_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/2'
bert_layer = hub.KerasLayer(module_url, trainable=True)

vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = bert_tokenization.FullTokenizer(vocab_file, do_lower_case)


# UTILITY FUNCTIONS
saved_model = tf.keras.models.load_model(
    f'{config.MODEL_PATH}/{config.MODEL_NAME}')


def bert_encode(texts, tokenizer, max_len=512):
    all_tokens = []
    all_masks = []
    all_segments = []

    for text in texts:
        text = tokenizer.tokenize(text)

        text = text[:max_len-2]
        input_sequence = ["[CLS]"] + text + ["[SEP]"]
        pad_len = max_len - len(input_sequence)

        tokens = tokenizer.convert_tokens_to_ids(
            input_sequence) + [0] * pad_len
        pad_masks = [1] * len(input_sequence) + [0] * pad_len
        segment_ids = [0] * max_len

        all_tokens.append(tokens)
        all_masks.append(pad_masks)
        all_segments.append(segment_ids)

    return np.array(all_tokens), np.array(all_masks), np.array(all_segments)


# FASTAPI

class Item(BaseModel):
    input_text: str


app = FastAPI()
origins = [
    "*"
    # "http://localhost",
    # "http://localhost:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def helloWorld():
    return {"message": "Welcome, I am CyberPolice! I will help you determine if a text is sexually harassing."}


@app.post("/predict")
async def predict(item: Item):
    """predicts if sentence is sexually harassing

    Parameters
    ----------
    item : Item
        BaseModel derived class object containing input_text(str).

    Returns
    -------
    dict
        Example dict
        {
            "confidence": 0.014952600002288818,
            "CyberPolice": "CYBER POLICE: says this sentence is not Sexually Harassing."
        }
    """
    inp = bert_encode([item.input_text], tokenizer, max_len=config.MAX_LEN)
    pred = saved_model.predict(inp)
    msg = 'CYBER POLICE: says this sentence is not Sexually Harassing.'
    if(pred[0][0] > 0.5):
        msg = 'CYBER POLICE: ALERT! This sentence is Sexually Harassing. Call 155260 or visit https://cybercrime.gov.in  to report this crime.'
    print(pred, pred[0][0], type(pred), type(pred[0][0]))
    return {"confidence": pred.item(), "CyberPolice": msg}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

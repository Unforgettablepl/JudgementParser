import sys
import torch
from IndicTransToolkit import IndicProcessor
from mosestokenizer import MosesSentenceSplitter
from nltk import sent_tokenize
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers.utils import is_flash_attn_2_available, is_flash_attn_greater_or_equal_2_10

flores_codes = {
    "asm_Beng": "as",
    "awa_Deva": "hi",
    "ben_Beng": "bn",
    "bho_Deva": "hi",
    "brx_Deva": "hi",
    "doi_Deva": "hi",
    "eng_Latn": "en",
    "gom_Deva": "kK",
    "guj_Gujr": "gu",
    "hin_Deva": "hi",
    "hne_Deva": "hi",
    "kan_Knda": "kn",
    "kas_Arab": "ur",
    "kas_Deva": "hi",
    "kha_Latn": "en",
    "lus_Latn": "en",
    "mag_Deva": "hi",
    "mai_Deva": "hi",
    "mal_Mlym": "ml",
    "mar_Deva": "mr",
    "mni_Beng": "bn",
    "mni_Mtei": "hi",
    "npi_Deva": "ne",
    "ory_Orya": "or",
    "pan_Guru": "pa",
    "san_Deva": "hi",
    "sat_Olck": "or",
    "snd_Arab": "ur",
    "snd_Deva": "hi",
    "tam_Taml": "ta",
    "tel_Telu": "te",
    "urd_Arab": "ur",
}

if not torch.cuda.is_available():
    print("CUDA not available. Exiting.")
    sys.exit(1)

ckpt_dir = "ai4bharat/indictrans2-en-indic-1B"
BATCH_SIZE = 4
DEVICE = "cuda"
HALF_PRECISION = True
EMPTY_CACHE_AFTER_BATCH = True

print("Using Batch Size:", BATCH_SIZE)
print("Using Device:", DEVICE)

ip = IndicProcessor(inference=True)
if is_flash_attn_2_available() and is_flash_attn_greater_or_equal_2_10():
    print("Using Flash Attention 2.0")
    attn_implementation = "flash_attention_2"
else:
    print("Using Eager Attention")
    attn_implementation = "eager"
tokenizer = AutoTokenizer.from_pretrained(ckpt_dir, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(
    ckpt_dir,
    trust_remote_code=True,
    attn_implementation=attn_implementation,
    low_cpu_mem_usage=True,
    quantization_config=None,
)
model = model.to(DEVICE)
if HALF_PRECISION:
    print("Using half precision")
    model.half()
model.eval()

print("Model loaded successfully")


def split_sentences(input_text):
    with MosesSentenceSplitter("en") as splitter:
        sents_moses = splitter([input_text])
    input_sentences = sents_moses
    input_sentences = [sent.replace("\xad", "") for sent in input_sentences]
    return input_sentences

def batch_translate(input_sentences,tgt_lang):
    translations = []
    for i in range(0, len(input_sentences), BATCH_SIZE):
        batch = input_sentences[i : i + BATCH_SIZE]
        batch = ip.preprocess_batch(batch, src_lang="eng_Latn", tgt_lang=tgt_lang)
        inputs = tokenizer(
            batch,
            truncation=True,
            padding="longest",
            return_tensors="pt",
            return_attention_mask=True,
        ).to(DEVICE)
        with torch.no_grad():
            generated_tokens = model.generate(
                **inputs,
                use_cache=True,
                min_length=0,
                max_length=256,
                num_beams=5,
                num_return_sequences=1,
            )
        with tokenizer.as_target_tokenizer():
            generated_tokens = tokenizer.batch_decode(
                generated_tokens.detach().cpu().tolist(),
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True,
            )
        translations += ip.postprocess_batch(generated_tokens, lang=tgt_lang)
        del inputs
        if EMPTY_CACHE_AFTER_BATCH: torch.cuda.empty_cache()
    translations = [sent.strip() for sent in translations]
    return translations


def translateParagraph(input_text, tgt_lang):
    if not tgt_lang in flores_codes:
        raise "Language not supported"
    input_sentences = split_sentences(input_text)
    translated_text = batch_translate(input_sentences,tgt_lang)
    return " ".join(translated_text)

if __name__ == "__main__":
    input_text = input("Enter the text to be translated: ")
    tgt_lang = "pan_Guru"
    translated_text = translateParagraph(input_text, tgt_lang)
    print("Translated text:")
    print(translated_text)
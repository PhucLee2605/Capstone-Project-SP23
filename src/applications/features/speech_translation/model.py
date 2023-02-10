from .preprocess import splitSentence
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re


def backBone(device='cpu'):
    model_name = "VietAI/envit5-translation"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

    return tokenizer, model



def infer(data, tokenizer, model, max_length, device='cpu'):
    predictions = list()
    for key, input, output in data:
        print(f"Start predict {key}")
        document = list()
        paragraphs = re.sub(r'(\n\s*){2,}', r'\n\n', input).split('\n')

        for para in paragraphs:
            if para == "":
                document.append("")
                continue
            if para[:3] != 'en:' and para[:3] != 'vi:':
                para = paragraphs[0][:3] + ' ' + para

            token_input = tokenizer(para, return_tensors="pt", padding=True).input_ids.to(device)
            decode_input = tokenizer.batch_decode(token_input, skip_special_tokens=True)[0]

            sentences = re.sub(' +', ' ', decode_input.strip())

            lstSen = splitSentence(sentences, 256)
            tok = tokenizer(lstSen, return_tensors="pt", padding=True).input_ids.to(device)
            result = model.generate(tok, max_length=max_length)
            result = tokenizer.batch_decode(result, skip_special_tokens=True)

            pred = '. '.join([chunk[4:] for chunk in result])

            document.append(pred)

        predictions.append(['\n'.join(document), output])

    return predictions

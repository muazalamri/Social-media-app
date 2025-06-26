import torch.nn.functional as F
from pickle import load
from transformers import AutoModel, AutoTokenizer
print('libs loaded')
input_texts = [
    "what is the capital of China?",
    "what is the capital of China?",
    "what is the capital of Usa?",
    "how to implement quick sort in python?",
    "北京",
    "快排算法介绍",
    "ما هي عاصمة الصين",
    "تجربة كرة القدم"
]
model_name_or_path = 'Alibaba-NLP/gte-multilingual-base'
tokenizer = load(open('tokenizer.pkl','rb'))
model = load(open('model.pkl','rb'))
def simualrty(text:str,listSentence:list[str]):
    input_texts=[text]+listSentence
    # Tokenize the input texts
    batch_dict = tokenizer(input_texts, max_length=8192, padding=True, truncation=True, return_tensors='pt')

    outputs = model(**batch_dict)

    dimension=768 # The output dimension of the output embedding, should be in [128, 768]
    embeddings = outputs.last_hidden_state[:, 0][:dimension]

    embeddings = F.normalize(embeddings, p=2, dim=1)
    scores = (embeddings[:1] @ embeddings[1:].T) * 100
    print(scores.tolist())
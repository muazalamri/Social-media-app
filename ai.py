'''# Use a pipeline as a high-level helper ;https://www.msn.com/ar-sa/money/news/%D8%A5%D8%AF%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D9%85%D8%AE%D8%A7%D8%B7%D8%B1-%D9%81%D9%8A-%D8%A7%D9%84%D8%B4%D8%B1%D9%83%D8%A7%D8%AA-%D8%A7%D9%84%D9%86%D8%A7%D8%B4%D8%A6%D8%A9-%D8%AE%D8%B7%D9%88%D8%A7%D8%AA-%D8%B9%D9%85%D9%84%D9%8A%D8%A9/ar-AA1AySsS?ocid=winp1taskbar&cvid=3c4a337dbff648b3d1959dfe197861cf&ei=23
from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B")
pipe(messages)
# Load model directly
from pickle import dump
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
dump(tokenizer, open('tokenizer.pkl', 'wb'))
dump(model, open('model.pkl', 'wb'))# Path: ai.py
import torch.nn.functional as F
from pickle import dump
from transformers import AutoModel, AutoTokenizer


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
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True)
dump(tokenizer, open('tokenizer.pkl', 'wb'))
dump(model, open('model.pkl', 'wb'))
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
# Load model directly
from pickle import dump
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
dump(tokenizer, open('tokenizer.pkl', 'wb'))
dump(model, open('model.pkl', 'wb'))# Path: ai.py
simualrty('احب اللعب الجماعي مع اصدقائي',listSentence=input_texts)
from transformers import AutoModelForCausalLM, AutoTokenizer
from hqq.engine.hf import HQQModelForCausalLM
from hqq.models.hf.base import AutoHQQHFModel

try:
 model = HQQModelForCausalLM.from_quantized("PrunaAI/ClosedCharacter-Peach-9B-8k-Roleplay-HQQ-1bit-smashed", device_map='auto')
except: 
 model = AutoHQQHFModel.from_quantized("PrunaAI/ClosedCharacter-Peach-9B-8k-Roleplay-HQQ-1bit-smashed")
tokenizer = AutoTokenizer.from_pretrained("ClosedCharacter/Peach-9B-8k-Roleplay")

input_ids = tokenizer("What is the color of prunes?,", return_tensors='pt').to(model.device)["input_ids"]

outputs = model.generate(input_ids, max_new_tokens=216)
tokenizer.decode(outputs[0])
'''
## Use a pipeline as a high-level helper
from transformers import pipeline

messages = [
    {"role": "user", "text": "Convert code to text<image>",'images':['C:\\Users\\ACER\\Downloads\\Zup-main\\html\\static\\images\\logo-full.png']},
]
pipe = pipeline("image-text-to-text", model="ds4sd/SmolDocling-256M-preview")
print(pipe(messages))
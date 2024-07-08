from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("openlm-research/llama-3b")
model = AutoModelForCausalLM.from_pretrained("openlm-research/llama-3b")

def generate_summary(content):
    inputs = tokenizer.encode("summarize: " + content, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# i dont think this works

import requests
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("output-small")
model.push_to_hub("RickBot")

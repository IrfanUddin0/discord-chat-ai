from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class GPT:
    model_name: str
    tokenizer: AutoTokenizer
    model: AutoModelForCausalLM

    @staticmethod
    def init():
        GPT.model_name = "microsoft/DialoGPT-large"

        GPT.tokenizer = AutoTokenizer.from_pretrained(GPT.model_name)
        GPT.model = AutoModelForCausalLM.from_pretrained(GPT.model_name)
        
    @staticmethod
    def make_prompt(text: str) -> str:
        input_ids = GPT.tokenizer.encode(text + GPT.tokenizer.eos_token, return_tensors="pt")
        
        chat_response_ids = GPT.model.generate(
            input_ids,
            max_length=1000,
            do_sample=True,
            top_k=100,
            temperature=0.75,
            pad_token_id=GPT.tokenizer.eos_token_id,
        )
        
        output = GPT.tokenizer.decode(chat_response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        return output
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM 
from peft import PeftModel
import argparse

def generate_prompt(text):
    # print("问：{}\n\n答：".format(text))
    return "问：{}\n\n答：".format(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_model', default=None, type=str, required=True)
    parser.add_argument('--lora_model', default=None, type=str, help="If None, perform inference on the base model")
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--repetition_penalty", type=float, default=1.6)
    parser.add_argument("--max_new_tokens", type=int, default=1024)
    args = parser.parse_args()
    
    load_type = torch.float16
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(args.base_model, trust_remote_code=True).half().cuda()
    if len(args.lora_model) > 0:
        model = PeftModel.from_pretrained(base_model, args.lora_model, torch_dtype=load_type, device_map='auto')
        print("Loaded lora model")
        model = model.merge_and_unload()
    else:
        model = base_model
    model.eval()

    text = '混凝土表面缺损的主要原因是什么？'
    response, history = model.chat(tokenizer, text)
    print(response)
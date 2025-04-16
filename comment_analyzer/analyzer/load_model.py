import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import gc

class ModelLoader:
    def __init__(self, model_name="microsoft/Phi-3-mini-128k-instruct", device_map="cuda", torch_dtype=torch.float16):
        self.model_name = model_name
        self.device_map = device_map
        self.torch_dtype = torch_dtype
        self.model = None
        self.tokenizer = None

    def load_model(self, BASE_DIR=os.path.dirname(os.path.abspath(__file__))):
        model_path = os.path.join(os.path.dirname(BASE_DIR), "models", "model")
        if self.model is not None:
            print("Model is already loaded.")
        elif os.path.exists(model_path):
            print("Loading model from local storage...")
            self.model = AutoModelForCausalLM.from_pretrained(model_path, 
                                                    device_map=self.device_map,
                                                    torch_dtype=self.torch_dtype,
                                                    trust_remote_code=True,
                                                    attn_implementation="eager" )
        else:
            print("Downloading model from huggingface...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map=self.device_map,
                torch_dtype=self.torch_dtype,
                trust_remote_code=True,
                attn_implementation="eager"
            )
            self.model.save_pretrained(os.path.join(os.path.dirname(BASE_DIR), "models", "model"))

    def load_tokenizer(self, BASE_DIR=os.path.dirname(os.path.abspath(__file__))):
        tokenizer_path = os.path.join(os.path.dirname(BASE_DIR), "models", "tokenizer")
        if self.tokenizer is not None:
            print("Tokenizer is already loaded.")
        elif os.path.exists(tokenizer_path):
            print("Loading tokenizer from local storage...")
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        else:
            print("Downloading tokenizer from huggingface...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.tokenizer.save_pretrained(os.path.join(os.path.dirname(BASE_DIR), "models", "tokenizer"))

    def load(self):
        torch.random.manual_seed(0)
        self.load_model()
        self.load_tokenizer()
        return self.model, self.tokenizer

    def clear_memory(self):
        del self.model
        del self.tokenizer
        torch.cuda.empty_cache()
        gc.collect()

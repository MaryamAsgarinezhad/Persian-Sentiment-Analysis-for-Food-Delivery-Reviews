from analyzer.preprocessing import Preprocessor
from .generate import GenerateAndPostprocess
from analyzer.load_model import ModelLoader

def analyze(data):
    # load the model and tokenizer
    model_loader = ModelLoader()
    model, tokenizer = model_loader.load()

    # preprocess the data
    preprocessor = Preprocessor(data)
    primary_inputs, primary_results = preprocessor.process()
    # generate and postprocess the results
    generator = GenerateAndPostprocess(model=model, tokenizer=tokenizer, primary_inputs=primary_inputs)
    results, raw_result = generator()
    return results, raw_result

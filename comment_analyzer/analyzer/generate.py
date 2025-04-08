import json
import transformers
import torch
import gc
import analyzer.prompt as prompt
import re

class GenerateAndPostprocess:
    def __init__(self, model=None, tokenizer=None, primary_inputs=None, prompt=prompt.get_prompt(), system_role=prompt.get_system_role(), service_list=[]):
        self.model = model
        self.tokenizer = tokenizer
        self.primary_inputs = primary_inputs
        self.primary_results = dict()
        self.service_list = service_list
        self.prompt = prompt
        self.system_role = system_role

    def separate_json(self, text):
        start = text.find('{')
        end = text.rfind('}') + 1
        json_text = text[start:end]
        try:
            json_text = json_text.replace('qualities', '"qualities"')
            json_text = json_text.replace('services', '"services"')
        except:
            pass
        return json_text

    def split_json(self, json_text):
        json_text = json_text.replace('""', '"')
        json_text = json_text.replace('\u200c', ' ')
        json_text = json_text.replace('```json', '')
        print(json_text)
        data = json.loads(json_text)
        qualities = data.get('qualities', [])
        services = data.get('services', [])
        food_overall = data.get('foods overall rating', "nan")
        return qualities, services, food_overall

    def process(self):
        texts = []
        for index, row in enumerate(self.primary_inputs):
            input_ids = self.tokenize(row)
            output_ids = self.analyze(input_ids)
            text = self.tokenizer.batch_decode(output_ids[:, input_ids.shape[1]:])[0]
            json_text = self.separate_json(text)
            qualities, services, food_overall = self.split_json(json_text)
            self.primary_results[index] = {}
            self.primary_results[index]['qualities'] = qualities
            self.primary_results[index]['foods overall rating'] = food_overall
            qualities, services = self.postprocess(qualities, services, row,)
            self.primary_results[index]['services'] = services
            results = self.primary_results
            try:
              text = text.split("```json")[1]
              text = text.split("```")[0]
            except:
              pass
            texts.append(text)
        return results, texts
            
    def analyze(self, input_ids):
        output_ids = self.model.generate(input_ids, max_new_tokens=2000)
        return output_ids
    
    def tokenize(self, inputs):
        prompt = self.prompt.format(order=inputs['foods'], comment=inputs['comment'], ingredients=inputs['materials'])
        messages = [{"role": "system",
            "content": f"{self.system_role}"},
        {"role": "user",
        "content": f"{prompt}"}]

        input_ids = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")
        
        return input_ids
        
    def postprocess(self, qualities, services, inputs):
        food_titels = list()
        for item in qualities:
            food_titels.append(item["food_title"])
        for index,food in enumerate(qualities):
            if food["food_title"] not in inputs["foods"]:
                #remove the food from the qualities
                qualities.pop(index)
        for food in inputs["foods"]:
            if food not in food_titels:
                #add the food to the qualities
                temp_dict = dict()
                temp_dict["food_title"] = food
                temp_dict["food_rate"] = "nan"
                qualities.append(temp_dict)
        
        for index, service in enumerate(services):
            if service["service_category"] not in self.service_list:
                services.pop(index)     
        return qualities, services
    
    def __call__(self,):
        response, raw_response = self.process()
        return response, raw_response
                
        
        
        
        
        
        

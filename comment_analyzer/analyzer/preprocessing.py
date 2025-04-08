import pandas as pd
import numpy as np
import json
import re
import ast

class Preprocessor:
    def __init__(self, data):
        if isinstance(data, pd.DataFrame):
            self.data = data
        elif isinstance(data, np.ndarray):
            self.data = pd.DataFrame(data)
        elif isinstance(data, dict):
            self.data = pd.DataFrame(data)
        elif isinstance(data, str):  # assuming data is a JSON file path
            json_data = json.load(data)
            self.data = pd.DataFrame(json_data)
        else:
            raise ValueError("Invalid data type. Please provide a pandas DataFrame, numpy array, dictionary, or JSON.")

    def process(self):
        comment_text_array = self.data['comment_text'].to_numpy()
        

        foods_text_array = self.data['foods'].to_numpy()
        primary_inputs = []
        primary_results = []
        for comment, food in zip(comment_text_array, foods_text_array):
            json_food = [ast.literal_eval(food)]
            current_materials = ""
            foods = list()
            for product in json_food:
                json_product = product
                current_materials = current_materials +" , "+ "{"+ json_product['product_title']+ " : " +json_product['product_description']+"}"
                foods.append(re.sub(r"\u200c", ' ', json_product['product_title']))
            primary_inputs.append({
                    "comment": re.sub(r"\u200c", ' ', comment),
                    "materials": re.sub(r"\u200c", ' ', current_materials),
                    "foods": foods
                })
            if 'qualities' in self.data.columns and 'services' in self.data.columns:
                qualities_text_array = self.data['qualities'].to_numpy()
                services_text_array = self.data['services'].to_numpy()
                for qualities, services in zip(qualities_text_array, services_text_array):
                    json_qualities = ast.literal_eval(qualities)
                    json_services = ast.literal_eval(services)
                    primary_results.append({
                            "comment_text": comment,
                            "order": foods,
                            "response_q": json_qualities,
                            "response_s": json_services
                        })
        return primary_inputs, primary_results

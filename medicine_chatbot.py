import numpy as np
import os
from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import re
import json
import time
from fuzzywuzzy import fuzz

class MedicineChatbot:
    def __init__(self):
        self.model_name = "paraphrase-albert-small-v2"
        self.model = SentenceTransformer(self.model_name)
        self.embeddings = self.load_embeddings()
        self.df = self.load_csv_data()


    def load_embeddings(self):
        embeddings_files = {
            "product_name": "embeddings/embeddings_product_name.npy",
            "salt_composition": "embeddings/embeddings_salt_composition.npy",
            "medicine_desc": "embeddings/embeddings_medicine_desc.npy",
            "side_effects": "embeddings/embeddings_side_effects.npy",
            "drug_interactions": "embeddings/embeddings_drug_interactions.npy"
        }
        return {column: np.load(path) for column, path in embeddings_files.items()}
    
    def load_csv_data(self):
        csv_path = os.path.expanduser("~/Desktop/medicine_data.csv")
        return pd.read_csv(csv_path)

    def get_query_embedding(self, query):
        return self.model.encode([query])

    def find_tablet_name(self, query_embedding):
        product_name_embeddings = self.embeddings["product_name"]
        similarity = cosine_similarity(query_embedding, product_name_embeddings)
        best_match_idx = similarity.argmax()
        best_similarity_score = similarity[0, best_match_idx]
        return best_match_idx, best_similarity_score

    def detect_intent(self, query):
        intents = {
            "side_effects": r'\bside effects\b',
            "salt_composition": r'\bcomposition\b',
            "drug_interactions": r'\binteractions\b',
            "medicine_desc": r'\bdescription\b',
            "dosage": r'\bdosage\b|\bdose\b',
            "uses": r'\buses\b|\bused for\b',
            "brand_generic": r'\bbrand\b|\bgeneric\b',
            "alternatives": r'\balternatives\b|\bsubstitutes\b'
        }
        for intent, pattern in intents.items():
            if re.search(pattern, query, re.IGNORECASE):
                return intent
        return "general"

    def fuzzy_match_tablet(self, query):
        best_match = max(self.df['product_name'], key=lambda x: fuzz.ratio(query.lower(), x.lower()))
        return best_match

    def generate_response(self, query, context=None):
        start_time = time.time()
        query_embedding = self.get_query_embedding(query)
        best_match_idx, similarity_score = self.find_tablet_name(query_embedding)
        response_time = time.time() - start_time

        tablet_info = self.df.iloc[best_match_idx]
        intent = self.detect_intent(query)

        response = {}
        confidence_score = similarity_score

        if similarity_score < 0.5:
            fuzzy_match = self.fuzzy_match_tablet(query)
            if fuzz.ratio(query.lower(), fuzzy_match.lower()) > 70:
                tablet_info = self.df[self.df['product_name'] == fuzzy_match].iloc[0]
                response["Message"] = f"Did you mean {fuzzy_match}? Here's the information:"
                confidence_score = fuzz.ratio(query.lower(), fuzzy_match.lower()) / 100
            else:
                response["Message"] = "The question is out of context. I'm just a medicine chatbot. I have information about specific tablets, their descriptions, and side effects."
                response["Suggestion"] = "Would you like to know more about a specific tablet? If so, please specify the tablet name."
                return response, confidence_score, response_time

        if intent == "side_effects":
            response["Side Effects"] = tablet_info["side_effects"]
        elif intent == "salt_composition":
            response["Salt Composition"] = tablet_info["salt_composition"]
        elif intent == "drug_interactions":
            response["Drug Interactions"] = tablet_info["drug_interactions"]
        elif intent == "medicine_desc":
            response["Medicine Description"] = tablet_info["medicine_desc"]
        elif intent == "dosage":
            response["Dosage"] = "Please consult a healthcare professional for dosage information."
        elif intent == "uses":
            response["Uses"] = tablet_info["medicine_desc"].split('.')[0]  # Assuming the first sentence describes the use
        elif intent == "brand_generic":
            response["Brand/Generic"] = f"{tablet_info['product_name']} is a brand name. For generic alternatives, please consult a pharmacist."
        elif intent == "alternatives":
            response["Alternatives"] = "For alternative medications, please consult a healthcare professional."
        else:
            response["Product Name"] = tablet_info["product_name"]
            response["Medicine Description"] = tablet_info["medicine_desc"]
            response["Side Effects"] = tablet_info["side_effects"]
            response["Drug Interactions"] = tablet_info["drug_interactions"]

        return response, confidence_score, response_time

    def get_random_tablet_info(self):
        random_tablet = self.df.sample(n=1).iloc[0]
        return {
            "Product Name": random_tablet["product_name"],
            "Description": random_tablet["medicine_desc"],
            "Side Effects": random_tablet["side_effects"],
            "Drug Interactions": random_tablet["drug_interactions"],
            "Salt Composition": random_tablet["salt_composition"]
        }

    def save_chat_history(self, chat_history, filename='logs/chat_history.json'):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing_history = json.load(f)
        else:
            existing_history = []

        existing_history.extend(chat_history)
        with open(filename, 'w') as f:
            json.dump(existing_history, f, indent=4)

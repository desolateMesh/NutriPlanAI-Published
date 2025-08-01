import os
import tensorflow as tf
from transformers import TFDistilBertForSequenceClassification, DistilBertTokenizerFast

class GoalClassifier:
    """
    A classifier to determine a user's primary health goal from freeform text.
    It uses a pre-trained DistilBERT model fine-tuned for sequence classification.
    """
    def __init__(self, model_path: str, tokenizer_path: str):
        """
        Initializes the GoalClassifier by loading the model, tokenizer,
        and dynamically setting the labels from the model's configuration.
        """
        print("-> Loading classifier model and tokenizer...")
        if not os.path.exists(model_path) or not os.path.exists(tokenizer_path):
            raise FileNotFoundError(
                f"Model or tokenizer not found. Searched paths:"
                f"\nModel: {os.path.abspath(model_path)}"
                f"\nTokenizer: {os.path.abspath(tokenizer_path)}"
            )
        
        self.model = TFDistilBertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(tokenizer_path)
        
        self.labels = [
            "weight_loss",      # 0
            "muscle_gain",      # 1
            "maintenance",      # 2
            "general_health",   # 3
            "weight_gain"       # 4
        ]

        
        print(f"-> Classifier loaded successfully with labels: {self.labels}")

    def classify(self, text: str) -> dict:
        """
        Classifies the given text into one of the predefined goal categories.

        Args:
            text (str): The user's goal description.

        Returns:
            dict: A dictionary containing the predicted 'label' and its 'confidence' score.
        """
        inputs = self.tokenizer(text, return_tensors="tf", truncation=True, padding=True)
        outputs = self.model(inputs).logits
        probabilities = tf.nn.softmax(outputs, axis=-1)[0]
        predicted_index = tf.argmax(probabilities).numpy()
        
        label = self.labels[predicted_index]
        confidence = probabilities[predicted_index].numpy()
        
        return {"label": label, "confidence": float(confidence)}
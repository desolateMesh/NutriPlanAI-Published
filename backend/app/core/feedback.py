# C:\Users\jrochau\projects\NutriPlan AI\backend\core\feedback.py

import pandas as pd
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import numpy as np

from app.db.models.feedback import Feedback as FeedbackModel
from app.db.models.meal import Meal

class FeedbackEngine:
    """
    Manages user-specific adaptive learning models using Naive Bayes.
    This engine learns from user-provided text feedback (likes/dislikes on meal names and tags)
    to predict the probability of a user liking other meals.
    """
    def __init__(self):
        self.user_models = {}

    def _get_model_for_user(self, user_id: int):
        """
        Retrieves or creates a model pipeline for a given user.
        A pipeline simplifies the process by chaining the vectorizer and classifier.
        """
        if user_id not in self.user_models:
            self.user_models[user_id] = {
                "model": make_pipeline(TfidfVectorizer(stop_words='english'), MultinomialNB()),
                "is_fitted": False
            }
        return self.user_models[user_id]

    def _get_feedback_data_for_user(self, db: Session, user_id: int) -> pd.DataFrame:
        """
        Retrieves all feedback for a specific user and prepares it for training.
        """
        query = db.query(
            FeedbackModel.rating,
            Meal.name,
            Meal.tags
        ).join(Meal, FeedbackModel.meal_id == Meal.id).filter(FeedbackModel.user_id == user_id)
        
        df = pd.read_sql(query.statement, db.bind)
        
        if df.empty:
            return pd.DataFrame()

        df['text_features'] = df['name'] + ' ' + df['tags'].apply(lambda x: ' '.join(x or []))

        df['target'] = (df['rating'] > 3).astype(int)
        
        return df[['text_features', 'target']]

    def train(self, db: Session, user_id: int):
        """
        Trains or retrains a specific user's feedback model.
        """
        user_model_data = self._get_model_for_user(user_id)
        model_pipeline = user_model_data["model"]
        
        feedback_df = self._get_feedback_data_for_user(db, user_id)

        if feedback_df.empty or feedback_df['target'].nunique() < 2:
            print(f"Insufficient or non-varied feedback data for user {user_id}. Cannot train model.")
            return

        X = feedback_df['text_features']
        y = feedback_df['target']

        model_pipeline.fit(X, y)
        user_model_data["is_fitted"] = True
        print(f"Feedback model for user {user_id} has been successfully trained.")

    def predict_score(self, meals: list[Meal], user_id: int) -> list[float]:
        """
        Predicts a "like" probability score for a list of meals for a specific user.
        """
        user_model_data = self._get_model_for_user(user_id)
        model_pipeline = user_model_data["model"]

        if not user_model_data["is_fitted"]:
            return [0.5] * len(meals)
        
        text_features = [m.name + ' ' + ' '.join(m.tags or []) for m in meals]

        probabilities = model_pipeline.predict_proba(text_features)
        like_probabilities = probabilities[:, 1]
        
        return like_probabilities.tolist()

    def get_top_features(self, user_id: int, n_features: int = 20) -> dict:
        """
        Extracts the most important words (features) the user's model has learned.
        This provides insight into the AI's decision-making process.
        """
        user_model_data = self._get_model_for_user(user_id)
        model_pipeline = user_model_data["model"]

        if not user_model_data["is_fitted"]:
            return {"message": "Model is not trained yet."}
        
        vectorizer = model_pipeline.named_steps['tfidfvectorizer']
        classifier = model_pipeline.named_steps['multinomialnb']

        feature_names = np.array(vectorizer.get_feature_names_out())

        liked_class_coef = classifier.feature_log_prob_[1]
        
        top_indices = liked_class_coef.argsort()[-n_features:][::-1]
        
        top_features = feature_names[top_indices]
        top_scores = liked_class_coef[top_indices]

        return dict(zip(top_features, top_scores))
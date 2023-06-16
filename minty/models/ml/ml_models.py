import pickle

import numpy as np
from flask import current_app
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.types import PickleType

from minty.extensions import db
from minty.models import Transaction


class Classifier(db.Model):
    __tablename__ = "classifiers"

    classifier_id = db.Column(INTEGER, primary_key=True)
    classifier_name = db.Column(VARCHAR(100), unique=True)
    classifier_model = db.Column(PickleType)
    date_filter = db.Column(DATE)
    is_trained = db.Column(BOOLEAN)
    accuracy = db.Column(NUMERIC(20, 4))
    is_active = db.Column(BOOLEAN, nullable=False, default=False)

    def __init__(self, classifier_name, date_filter):
        self.vectorizer = CountVectorizer()
        self.classifier = DecisionTreeClassifier()
        self.is_trained = False
        self.accuracy = None
        self.classifier_name = classifier_name
        self.date_filter = date_filter
        self.test_size = 0.20
        self.random_state = 42

    def _test_accuracy(self, all_features, all_answers, test_size, random_state):
        features_train, features_test, answers_train, answers_test = train_test_split(
            all_features, all_answers, test_size=test_size, random_state=random_state
        )
        self.classifier.fit(features_train, answers_train)
        category_pred = self.classifier.predict(features_test)
        accuracy = accuracy_score(answers_test, category_pred)
        current_app.logger.info(f"Accuracy: {accuracy}")
        return accuracy

    def _get_ml_data(self, date_filter):
        transaction_descriptions = []
        transaction_amounts = []
        categories = []
        account_ids = []
        encoder = OneHotEncoder(sparse_output=False)

        transactions = (
            (
                Transaction.query.with_entities(
                    Transaction.transaction_date,
                    Transaction.transaction_description,
                    Transaction.transaction_amount,
                    Transaction.custom_category_id,
                    Transaction.account_id,
                )
            )
            .filter(Transaction.transaction_date >= date_filter)
            .filter(Transaction.custom_category_id != -1)
        )

        for transaction in transactions:
            transaction_descriptions.append(transaction.transaction_description)
            transaction_amounts.append(transaction.transaction_amount)
            account_ids.append(transaction.account_id)
            categories.append(transaction.custom_category_id)

        del transactions

        transaction_descriptions_v = self.vectorizer.fit_transform(
            transaction_descriptions
        )
        transaction_amounts_a = np.array(transaction_amounts).reshape(-1, 1)
        account_ids_a = np.array(account_ids).reshape(-1, 1)

        del transaction_descriptions
        del transaction_amounts
        del account_ids

        all_features = np.concatenate(
            (
                transaction_descriptions_v.toarray(),
                transaction_amounts_a,
                account_ids_a,
            ),
            axis=1,
        )
        all_answers = encoder.fit_transform(np.array(categories).reshape(-1, 1))

        return all_features, all_answers

    def train(self, date_filter):
        features, answers = self._get_ml_data(date_filter=date_filter)
        self.accuracy = self._test_accuracy(
            all_features=features,
            all_answers=answers,
            test_size=self.test_size,
            random_state=self.random_state,
        )
        self.classifier.fit(features, answers)
        self.is_trained = True

    def classify(self, transaction_features):
        if not self.is_trained:
            raise Exception("Classifier not trained yet.")
        transaction_features_vectorized = self.vectorizer.transform(
            transaction_features
        )
        predicted_category = self.classifier.predict(transaction_features_vectorized)
        return predicted_category

    def save_model(self):
        current_app.logger.info(f"Saving Classifier: {self.classifier_name}")
        self.classifier_model = pickle.dumps(self)

    @classmethod
    def get_by_classifier_name(cls, classifier_name):
        return cls.query.filter_by(classifier_name=classifier_name).first()

    @classmethod
    def load_model(cls, classifier_name):
        current_app.logger.info(f"Loading Classifier: {classifier_name}")
        classifier = cls.get_by_classifier_name(classifier_name=classifier_name)
        return pickle.loads(classifier.classifier_model)

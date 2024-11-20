import pickle
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from config.settings.base import BASE_DIR
from skillcobra.core.models import ProfanityModel

training_data = [
    (record["message"], record["profanity_score"])
    for record in ProfanityModel.objects.values("message", "profanity_score")
]
text, labels = zip(*training_data, strict=False)


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(text)

model = LogisticRegression()
model.fit(X, labels)


def save_training_model():
    with Path.open(str(BASE_DIR / "models" / "profanity_model.pkl"), "wb") as f:
        pickle.dump((vectorizer, model), f)

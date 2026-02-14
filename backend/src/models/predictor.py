from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import joblib
import os


class ShelfLifePredictor:
    def __init__(self, n_estimators=100, max_depth=10, random_state=42):
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
        self.is_trained = False
        self.feature_importance = None
        self.best_params = None

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        self.is_trained = True
        self.feature_importance = dict(zip(X_train.columns, self.model.feature_importances_))
        return self

    def predict(self, X):
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        predictions = self.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)

        metrics = {
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'predictions': predictions.tolist(),
            'actual': y_test.tolist()
        }

        return metrics

    def cross_validate(self, X, y, cv=5):
        scores = cross_val_score(self.model, X, y, cv=cv, scoring='neg_mean_absolute_error')
        return {
            'mean_mae': -scores.mean(),
            'std_mae': scores.std(),
            'cv_scores': (-scores).tolist()
        }

    def hyperparameter_tune(self, X_train, y_train):
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15, 20],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }

        grid_search = GridSearchCV(
            RandomForestRegressor(random_state=42, n_jobs=-1),
            param_grid,
            cv=5,
            scoring='neg_mean_absolute_error',
            n_jobs=-1
        )

        grid_search.fit(X_train, y_train)
        self.model = grid_search.best_estimator_
        self.is_trained = True
        self.feature_importance = dict(zip(X_train.columns, self.model.feature_importances_))
        self.best_params = grid_search.best_params_
        
        return self.best_params

    def get_feature_importance(self, top_n=10):
        if not self.is_trained:
            raise ValueError("Model must be trained first")

        sorted_importance = sorted(
            self.feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return dict(sorted_importance[:top_n])

    def save(self, filepath):
        model_data = {
            'model': self.model,
            'is_trained': self.is_trained,
            'feature_importance': self.feature_importance,
            'best_params': self.best_params
        }
        joblib.dump(model_data, filepath)

    def load(self, filepath):
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.is_trained = model_data['is_trained']
        self.feature_importance = model_data['feature_importance']
        self.best_params = model_data['best_params']
        return self

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing.preprocessor import DataPreprocessor, load_data
from src.feature_engineering.engineer import FeatureEngineer
from src.models.predictor import ShelfLifePredictor
import json
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np


def train_model():
    print("Loading data...")
    X, y = load_data('data/food_shelf_life.csv')

    print("\nData shape:", X.shape)
    print("Target distribution:")
    print(y.describe())

    print("\nInitializing preprocessor...")
    preprocessor = DataPreprocessor()
    X_processed = preprocessor.fit_transform(X)

    print("Initializing feature engineer...")
    feature_engineer = FeatureEngineer()
    X_featured = feature_engineer.transform(X_processed)

    print("\nFeature columns:")
    print(X_featured.columns.tolist())

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X_featured, y, test_size=0.2, random_state=42
    )

    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")

    print("\n" + "="*60)
    print("Training Ensemble Model for High Accuracy (97%+)")
    print("="*60)

    rf_params = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 15, 20, 25, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'max_features': ['sqrt', 'log2', None]
    }

    gb_params = {
        'n_estimators': [100, 200],
        'max_depth': [10, 15, 20, 25, None],
        'learning_rate': [0.01, 0.05, 0.1],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }

    print("\n[1/4] Tuning Random Forest with RandomizedSearchCV...")
    rf_search = RandomizedSearchCV(
        RandomForestRegressor(random_state=42, n_jobs=-1),
        rf_params,
        n_iter=50,
        cv=5,
        scoring='neg_mean_absolute_error',
        n_jobs=-1,
        random_state=42
    )

    rf_search.fit(X_train, y_train)
    rf_best = rf_search.best_estimator_
    print(f"Best RF MAE: {-rf_search.best_score_:.3f}")

    print("\n[2/4] Tuning Gradient Boosting with RandomizedSearchCV...")
    gb_search = RandomizedSearchCV(
        GradientBoostingRegressor(random_state=42),
        gb_params,
        n_iter=50,
        cv=5,
        scoring='neg_mean_absolute_error',
        n_jobs=-1,
        random_state=42
    )

    gb_search.fit(X_train, y_train)
    gb_best = gb_search.best_estimator_
    print(f"Best GB MAE: {-gb_search.best_score_:.3f}")

    print("\n[3/4] Creating Voting Ensemble...")
    voting_regressor = VotingRegressor(
        estimators=[
            ('rf', rf_best),
            ('gb', gb_best)
        ],
        n_jobs=-1
    )

    voting_regressor.fit(X_train, y_train)
    print("Voting ensemble trained!")

    print("\n[4/4] Evaluating models...")

    rf_pred = rf_best.predict(X_test)
    gb_pred = gb_best.predict(X_test)
    voting_pred = voting_regressor.predict(X_test)

    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_r2 = r2_score(y_test, rf_pred)

    gb_mae = mean_absolute_error(y_test, gb_pred)
    gb_r2 = r2_score(y_test, gb_pred)

    voting_mae = mean_absolute_error(y_test, voting_pred)
    voting_r2 = r2_score(y_test, voting_pred)
    voting_rmse = np.sqrt(mean_squared_error(y_test, voting_pred))

    print("\n" + "="*60)
    print("Model Performance Comparison")
    print("="*60)
    print(f"{'Model':<20} {'MAE (days)':<15} {'R² Score':<12} {'Accuracy':<10}")
    print("-"*60)
    print(f"{'Random Forest':<20} {rf_mae:<15.3f} {rf_r2:<12.4f} {max(0, (1-rf_mae/90)*100):<10.1f}%")
    print(f"{'Gradient Boosting':<20} {gb_mae:<15.3f} {gb_r2:<12.4f} {max(0, (1-gb_mae/90)*100):<10.1f}%")
    print(f"{'Voting Ensemble':<20} {voting_mae:<15.3f} {voting_r2:<12.4f} {max(0, (1-voting_mae/90)*100):<10.1f}%")
    print("="*60)

    if voting_r2 >= 0.97:
        print("\n✅ SUCCESS! Achieved 97%+ accuracy (R² >= 0.97)")
        print(f"   Final R² Score: {voting_r2:.4f}")
        print(f"   Final MAE: {voting_mae:.3f} days")
    elif voting_r2 >= 0.90:
        print("\n✅ GOOD! High accuracy achieved (R² >= 0.90)")
        print(f"   Final R² Score: {voting_r2:.4f}")
        print(f"   Final MAE: {voting_mae:.3f} days")
    else:
        print(f"\n⚠️  Accuracy below target (R² = {voting_r2:.4f})")
        print("   Consider adding more training data")

    print("\nCross-validation results...")
    cv_scores = cross_val_score(voting_regressor, X_featured, y, cv=10, scoring='r2', n_jobs=-1)
    print(f"Mean R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"Min R²: {cv_scores.min():.4f}")
    print(f"Max R²: {cv_scores.max():.4f}")

    print("\nFeature Importances (from best Random Forest):")
    importance = dict(zip(X_featured.columns, rf_best.feature_importances_))
    sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)

    for feat, imp in sorted_importance[:15]:
        print(f"  {feat:<30} {imp:.4f}")

    print("\nSaving best model...")
    os.makedirs('models', exist_ok=True)

    import joblib
    best_model = voting_regressor if voting_r2 >= 0.90 else rf_best

    joblib.dump(best_model, 'models/shelf_life_predictor.pkl')
    print("Model saved successfully as: models/shelf_life_predictor.pkl")

    preprocessor.save('models/preprocessor.pkl')
    print("Preprocessor saved successfully as: models/preprocessor.pkl")

    return best_model, preprocessor


if __name__ == '__main__':
    train_model()

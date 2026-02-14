import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing.preprocessor import DataPreprocessor, load_data
from src.feature_engineering.engineer import FeatureEngineer
import json
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor, StackingRegressor, ExtraTreesRegressor
from sklearn.linear_model import Ridge
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
        X_featured, y, test_size=0.15, random_state=42
    )

    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")

    print("\n" + "="*60)
    print("Training Advanced Ensemble Model for 97%+ Accuracy")
    print("="*60)

    rf_params = {
        'n_estimators': [100, 200, 300, 400],
        'max_depth': [10, 15, 20, 25, 30, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None],
        'bootstrap': [True, False]
    }

    et_params = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 15, 20, 25, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'max_features': ['sqrt', 'log2']
    }

    gb_params = {
        'n_estimators': [100, 200, 300],
        'max_depth': [5, 10, 15, 20, None],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'subsample': [0.8, 0.9, 1.0]
    }

    print("\n[1/5] Tuning Random Forest...")
    rf_search = RandomizedSearchCV(
        RandomForestRegressor(random_state=42, n_jobs=-1),
        rf_params,
        n_iter=100,
        cv=5,
        scoring='neg_mean_absolute_error',
        n_jobs=-1,
        random_state=42
    )

    rf_search.fit(X_train, y_train)
    rf_best = rf_search.best_estimator_
    print(f"Best RF MAE: {-rf_search.best_score_:.3f}")

    print("\n[2/5] Tuning Extra Trees...")
    et_search = RandomizedSearchCV(
        ExtraTreesRegressor(random_state=42, n_jobs=-1),
        et_params,
        n_iter=80,
        cv=5,
        scoring='neg_mean_absolute_error',
        n_jobs=-1,
        random_state=42
    )

    et_search.fit(X_train, y_train)
    et_best = et_search.best_estimator_
    print(f"Best ET MAE: {-et_search.best_score_:.3f}")

    print("\n[3/5] Tuning Gradient Boosting...")
    gb_search = RandomizedSearchCV(
        GradientBoostingRegressor(random_state=42),
        gb_params,
        n_iter=80,
        cv=5,
        scoring='neg_mean_absolute_error',
        n_jobs=-1,
        random_state=42
    )

    gb_search.fit(X_train, y_train)
    gb_best = gb_search.best_estimator_
    print(f"Best GB MAE: {-gb_search.best_score_:.3f}")

    print("\n[4/5] Creating Advanced Ensemble (Voting)...")
    voting_regressor = VotingRegressor(
        estimators=[
            ('rf', rf_best),
            ('et', et_best),
            ('gb', gb_best)
        ],
        n_jobs=-1
    )

    voting_regressor.fit(X_train, y_train)
    print("Voting ensemble trained!")

    print("\n[5/5] Creating Advanced Ensemble (Stacking)...")
    stacking_regressor = StackingRegressor(
        estimators=[
            ('rf', rf_best),
            ('et', et_best),
            ('gb', gb_best)
        ],
        final_estimator=Ridge(random_state=42),
        n_jobs=-1
    )

    stacking_regressor.fit(X_train, y_train)
    print("Stacking ensemble trained!")

    print("\n" + "="*60)
    print("Model Performance Comparison")
    print("="*60)
    print(f"{'Model':<25} {'MAE':<12} {'R2':<10} {'Accuracy':<10}")
    print("-"*60)

    rf_pred = rf_best.predict(X_test)
    et_pred = et_best.predict(X_test)
    gb_pred = gb_best.predict(X_test)
    voting_pred = voting_regressor.predict(X_test)
    stacking_pred = stacking_regressor.predict(X_test)

    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_r2 = r2_score(y_test, rf_pred)
    rf_acc = max(0, (1 - rf_mae/90) * 100)

    et_mae = mean_absolute_error(y_test, et_pred)
    et_r2 = r2_score(y_test, et_pred)
    et_acc = max(0, (1 - et_mae/90) * 100)

    gb_mae = mean_absolute_error(y_test, gb_pred)
    gb_r2 = r2_score(y_test, gb_pred)
    gb_acc = max(0, (1 - gb_mae/90) * 100)

    voting_mae = mean_absolute_error(y_test, voting_pred)
    voting_r2 = r2_score(y_test, voting_pred)
    voting_acc = max(0, (1 - voting_mae/90) * 100)
    voting_rmse = np.sqrt(mean_squared_error(y_test, voting_pred))

    stacking_mae = mean_absolute_error(y_test, stacking_pred)
    stacking_r2 = r2_score(y_test, stacking_pred)
    stacking_acc = max(0, (1 - stacking_mae/90) * 100)

    print(f"{'Random Forest':<25} {rf_mae:<12.3f} {rf_r2:<10.4f} {rf_acc:<10.1f}%")
    print(f"{'Extra Trees':<25} {et_mae:<12.3f} {et_r2:<10.4f} {et_acc:<10.1f}%")
    print(f"{'Gradient Boosting':<25} {gb_mae:<12.3f} {gb_r2:<10.4f} {gb_acc:<10.1f}%")
    print(f"{'Voting Ensemble':<25} {voting_mae:<12.3f} {voting_r2:<10.4f} {voting_acc:<10.1f}%")
    print(f"{'Stacking Ensemble':<25} {stacking_mae:<12.3f} {stacking_r2:<10.4f} {stacking_acc:<10.1f}%")
    print("="*60)

    if stacking_r2 >= 0.97:
        print("\nSUCCESS! Achieved 97%+ accuracy (R2 >= 0.97)")
        print(f"   Final R2 Score: {stacking_r2:.4f}")
        print(f"   Final MAE: {stacking_mae:.3f} days")
    elif stacking_r2 >= 0.95:
        print("\nEXCELLENT! Very high accuracy achieved (R2 >= 0.95)")
        print(f"   Final R2 Score: {stacking_r2:.4f}")
        print(f"   Final MAE: {stacking_mae:.3f} days")
    elif stacking_r2 >= 0.90:
        print("\nGOOD! High accuracy achieved (R2 >= 0.90)")
        print(f"   Final R2 Score: {stacking_r2:.4f}")
        print(f"   Final MAE: {stacking_mae:.3f} days")
    else:
        print(f"\nAccuracy: {stacking_r2:.4f} (Target: 0.97)")
        print("   Consider adding more training data")

    print("\nCross-validation results...")
    cv_scores = cross_val_score(stacking_regressor, X_featured, y, cv=10, scoring='r2', n_jobs=-1)
    print(f"Mean R2: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
    print(f"Min R2: {cv_scores.min():.4f}")
    print(f"Max R2: {cv_scores.max():.4f}")

    print("\nFeature Importances (from best model):")
    importance = dict(zip(X_featured.columns, rf_best.feature_importances_))
    sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)

    for feat, imp in sorted_importance[:15]:
        print(f"  {feat:<35} {imp:.4f}")

    print("\nSaving best model...")
    os.makedirs('models', exist_ok=True)

    import joblib
    
    best_model = stacking_regressor
    best_mae = stacking_mae
    best_r2 = stacking_r2

    joblib.dump(best_model, 'models/shelf_life_predictor.pkl')
    print(f"Model saved: models/shelf_life_predictor.pkl")
    print(f"Performance: R2={best_r2:.4f}, MAE={best_mae:.3f} days")

    preprocessor.save('models/preprocessor.pkl')
    print("Preprocessor saved: models/preprocessor.pkl")

    print(f"\nFinal Accuracy: {best_r2*100:.1f}%")
    
    return best_model, preprocessor


if __name__ == '__main__':
    train_model()

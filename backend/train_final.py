import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing.preprocessor import DataPreprocessor
import pandas as pd
import numpy as np

try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except:
    HAS_XGB = False
    print("XGBoost not available, using GradientBoosting")

try:
    from lightgbm import LGBMRegressor
    HAS_LGBM = True
except:
    HAS_LGBM = False
    print("LightGBM not available, using GradientBoosting")

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor, StackingRegressor, ExtraTreesRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from src.models.predictor import ShelfLifePredictor
from src.feature_engineering.engineer import FeatureEngineer
import joblib


def load_data(filepath):
    df = pd.read_csv(filepath)
    X = df.drop('remaining_shelf_life', axis=1)
    y = df['remaining_shelf_life']
    return X, y


def train_model():
    print("="*80)
    print("Training High Accuracy Model (97%+ Target)")
    print("="*80)
    print()
    
    print("Loading data...")
    X, y = load_data('data/food_shelf_life.csv')

    print(f"\nDataset size: {X.shape[0]} samples")
    print("\nTarget distribution:")
    print(y.describe())

    print("\nInitializing preprocessor...")
    preprocessor = DataPreprocessor()
    X_processed = preprocessor.fit_transform(X)

    print("Initializing feature engineer...")
    feature_engineer = FeatureEngineer()
    X_featured = feature_engineer.transform(X_processed)

    print(f"\nFeature columns ({X_featured.shape[1]}):")
    for i, col in enumerate(X_featured.columns, 1):
        print(f"  {i:2d}. {col}")

    X_train, X_test, y_train, y_test = train_test_split(
        X_featured, y, test_size=0.15, random_state=42
    )

    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")

    print("\n" + "="*80)
    print("PHASE 1: Base Model Training")
    print("="*80)

    print("\n[1/3] Tuning Random Forest...")
    rf_params = {
        'n_estimators': [100, 200, 300, 400, 500],
        'max_depth': [10, 15, 20, 25, 30, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None],
        'bootstrap': [True, False]
    }

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

    print("\n[2/3] Tuning Gradient Boosting...")
    gb_params = {
        'n_estimators': [100, 200, 300, 400],
        'max_depth': [5, 10, 15, 20, 25, None],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'subsample': [0.8, 0.9, 1.0]
    }

    gb_search = RandomizedSearchCV(
        GradientBoostingRegressor(random_state=42),
        gb_params,
        n_iter=100,
        cv=5,
        scoring='neg_mean_absolute_error',
        n_jobs=-1,
        random_state=42
    )

    gb_search.fit(X_train, y_train)
    gb_best = gb_search.best_estimator_
    print(f"Best GB MAE: {-gb_search.best_score_:.3f}")

    print("\n[3/3] Tuning Extra Trees...")
    et_params = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 15, 20, 25, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2']
    }

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

    print("\n" + "="*80)
    print("PHASE 2: Advanced Model Training")
    print("="*80)

    if HAS_XGB:
        print("\n[XGBoost] Tuning XGBoost...")
        xgb_params = {
            'n_estimators': [100, 200, 300, 400, 500],
            'max_depth': [5, 10, 15, 20],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'min_child_weight': [1, 3, 5],
            'subsample': [0.8, 0.9, 1.0],
            'colsample_bytree': [0.8, 0.9, 1.0]
        }

        xgb_search = RandomizedSearchCV(
            XGBRegressor(random_state=42, n_jobs=-1),
            xgb_params,
            n_iter=100,
            cv=5,
            scoring='neg_mean_absolute_error',
            n_jobs=-1,
            random_state=42
        )

        xgb_search.fit(X_train, y_train)
        xgb_best = xgb_search.best_estimator_
        print(f"Best XGBoost MAE: {-xgb_search.best_score_:.3f}")

        xgb_pred = xgb_best.predict(X_test)
        xgb_mae = mean_absolute_error(y_test, xgb_pred)
        xgb_r2 = r2_score(y_test, xgb_pred)
        xgb_acc = max(0, (1 - xgb_mae/90) * 100)
        print(f"XGBoost Test: MAE={xgb_mae:.3f} days, R2={xgb_r2:.4f}, Accuracy={xgb_acc:.1f}%")
    elif HAS_LGBM:
        print("\n[LightGBM] Tuning LightGBM...")
        lgbm_params = {
            'n_estimators': [100, 200, 300, 400, 500],
            'max_depth': [5, 10, 15, 20],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'num_leaves': [15, 31, 63, 127],
            'min_child_samples': [5, 10, 20],
            'subsample': [0.8, 0.9, 1.0],
            'colsample_bytree': [0.8, 0.9, 1.0]
        }

        lgbm_search = RandomizedSearchCV(
            LGBMRegressor(random_state=42, n_jobs=-1, verbose=-1),
            lgbm_params,
            n_iter=100,
            cv=5,
            scoring='neg_mean_absolute_error',
            n_jobs=-1,
            random_state=42
        )

        lgbm_search.fit(X_train, y_train)
        lgbm_best = lgbm_search.best_estimator_
        print(f"Best LightGBM MAE: {-lgbm_search.best_score_:.3f}")

        lgbm_pred = lgbm_best.predict(X_test)
        lgbm_mae = mean_absolute_error(y_test, lgbm_pred)
        lgbm_r2 = r2_score(y_test, lgbm_pred)
        lgbm_acc = max(0, (1 - lgbm_mae/90) * 100)
        print(f"LightGBM Test: MAE={lgbm_mae:.3f} days, R2={lgbm_r2:.4f}, Accuracy={lgbm_acc:.1f}%")
    else:
        print("\n[XGBoost/LightGBM] Not available, skipping...")

    print("\n" + "="*80)
    print("PHASE 3: Ensemble Creation")
    print("="*80)

    print("\n[1/2] Creating Voting Ensemble...")
    voting_estimators = [
        ('rf', rf_best),
        ('gb', gb_best),
        ('et', et_best)
    ]

    if HAS_XGB:
        voting_estimators.append(('xgb', xgb_best))
    elif HAS_LGBM:
        voting_estimators.append(('lgbm', lgbm_best))

    voting_regressor = VotingRegressor(
        estimators=voting_estimators,
        n_jobs=-1
    )

    voting_regressor.fit(X_train, y_train)
    print("Voting ensemble trained!")

    print("\n[2/2] Creating Stacking Ensemble...")
    stacking_estimators = [
        ('rf', rf_best),
        ('gb', gb_best),
        ('et', et_best)
    ]

    if HAS_XGB:
        stacking_estimators.append(('xgb', xgb_best))
    elif HAS_LGBM:
        stacking_estimators.append(('lgbm', lgbm_best))

    stacking_regressor = StackingRegressor(
        estimators=stacking_estimators,
        final_estimator=Ridge(random_state=42),
        n_jobs=-1
    )

    stacking_regressor.fit(X_train, y_train)
    print("Stacking ensemble trained!")

    print("\n" + "="*80)
    print("FINAL MODEL EVALUATION")
    print("="*80)

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
    stacking_rmse = np.sqrt(mean_squared_error(y_test, stacking_pred))

    print(f"\n{'Model':<30} {'MAE':<12} {'R2':<10} {'Accuracy':<10}")
    print("-"*60)
    print(f"{'Random Forest':<30} {rf_mae:<12.3f} {rf_r2:<10.4f} {rf_acc:<10.1f}%")
    print(f"{'Extra Trees':<30} {et_mae:<12.3f} {et_r2:<10.4f} {et_acc:<10.1f}%")
    print(f"{'Gradient Boosting':<30} {gb_mae:<12.3f} {gb_r2:<10.4f} {gb_acc:<10.1f}%")

    if HAS_XGB:
        xgb_mae = mean_absolute_error(y_test, xgb_best.predict(X_test))
        xgb_r2 = r2_score(y_test, xgb_best.predict(X_test))
        xgb_acc = max(0, (1 - xgb_mae/90) * 100)
        print(f"{'XGBoost':<30} {xgb_mae:<12.3f} {xgb_r2:<10.4f} {xgb_acc:<10.1f}%")
    elif HAS_LGBM:
        lgbm_mae = mean_absolute_error(y_test, lgbm_best.predict(X_test))
        lgbm_r2 = r2_score(y_test, lgbm_best.predict(X_test))
        lgbm_acc = max(0, (1 - lgbm_mae/90) * 100)
        print(f"{'LightGBM':<30} {lgbm_mae:<12.3f} {lgbm_r2:<10.4f} {lgbm_acc:<10.1f}%")

    print(f"{'Voting Ensemble':<30} {voting_mae:<12.3f} {voting_r2:<10.4f} {voting_acc:<10.1f}%")
    print(f"{'Stacking Ensemble':<30} {stacking_mae:<12.3f} {stacking_r2:<10.4f} {stacking_acc:<10.1f}%")

    print("="*80)

    if stacking_r2 >= 0.97:
        print("\nSUCCESS! Achieved 97%+ accuracy")
        print(f"   Final R2 Score: {stacking_r2:.4f}")
        print(f"   Final MAE: {stacking_mae:.3f} days")
        best_model = stacking_regressor
        best_name = "Stacking Ensemble"
        best_mae = stacking_mae
        best_r2 = stacking_r2
        best_acc = stacking_acc
    elif stacking_r2 >= 0.90:
        print("\nEXCELLENT! High accuracy achieved")
        print(f"   Final R2 Score: {stacking_r2:.4f}")
        print(f"   Final MAE: {stacking_mae:.3f} days")
        best_model = stacking_regressor
        best_name = "Stacking Ensemble"
        best_mae = stacking_mae
        best_r2 = stacking_r2
        best_acc = stacking_acc
    elif stacking_r2 >= voting_r2:
        print("\nVoting ensemble performed better!")
        print(f"   Final R2 Score: {voting_r2:.4f}")
        print(f"   Final MAE: {voting_mae:.3f} days")
        best_model = voting_regressor
        best_name = "Voting Ensemble"
        best_mae = voting_mae
        best_r2 = voting_r2
        best_acc = voting_acc
    else:
        print(f"\nGradient Boosting performed best")
        print(f"   Final R2 Score: {gb_r2:.4f}")
        print(f"   Final MAE: {gb_mae:.3f} days")
        best_model = gb_best
        best_name = "Gradient Boosting"
        best_mae = gb_mae
        best_r2 = gb_r2
        best_acc = gb_acc

    print("\nCross-validation results...")
    cv_scores = cross_val_score(best_model, X_featured, y, cv=10, scoring='r2', n_jobs=-1)
    print(f"Mean R2: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
    print(f"Min R2: {cv_scores.min():.4f}")
    print(f"Max R2: {cv_scores.max():.4f}")

    print("\nFeature Importances:")
    if hasattr(best_model, 'feature_importances_'):
        importance = dict(zip(X_featured.columns, best_model.feature_importances_))
        sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)

        for i, (feat, imp) in enumerate(sorted_importance[:15], 1):
            print(f"  {i:2d}. {feat:<35} {imp:.4f}")

    print("\nSaving best model...")
    os.makedirs('models', exist_ok=True)

    joblib.dump(best_model, 'models/shelf_life_predictor.pkl')
    print(f"Model saved: models/shelf_life_predictor.pkl")
    print(f"Best Model: {best_name}")
    print(f"Performance: R2={best_r2:.4f}, MAE={best_mae:.3f} days")

    preprocessor.save('models/preprocessor.pkl')
    print("Preprocessor saved: models/preprocessor.pkl")

    print(f"\nFinal Accuracy: {best_r2*100:.1f}%")

    return best_model, preprocessor


if __name__ == '__main__':
    train_model()

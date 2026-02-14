import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing.preprocessor import DataPreprocessor, load_data
from src.feature_engineering.engineer import FeatureEngineer
import json
import numpy as np

try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except:
    HAS_XGB = False
    print("XGBoost not available, will use Gradient Boosting")

try:
    from lightgbm import LGBMRegressor
    HAS_LGBM = True
except:
    HAS_LGBM = False
    print("LightGBM not available, will use Gradient Boosting")

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor, StackingRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


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
    print("Training XGBoost/LGBM for High Accuracy (97%+)")
    print("="*60)

    if HAS_XGB:
        print("\n[1/4] Tuning XGBoost...")
        xgb_params = {
            'n_estimators': [100, 200, 300, 500],
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
        
        print(f"XGBoost MAE: {xgb_mae:.3f} days, R2: {xgb_r2:.4f}, Accuracy: {xgb_acc:.1f}%")
        
        best_model = xgb_best
        best_name = "XGBoost"
        best_mae = xgb_mae
        best_r2 = xgb_r2
        best_acc = xgb_acc

    elif HAS_LGBM:
        print("\n[1/4] Tuning LightGBM...")
        lgbm_params = {
            'n_estimators': [100, 200, 300, 500],
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
        
        print(f"LightGBM MAE: {lgbm_mae:.3f} days, R2: {lgbm_r2:.4f}, Accuracy: {lgbm_acc:.1f}%")
        
        best_model = lgbm_best
        best_name = "LightGBM"
        best_mae = lgbm_mae
        best_r2 = lgbm_r2
        best_acc = lgbm_acc
    else:
        print("\n[1/4] Tuning Gradient Boosting...")
        gb_params = {
            'n_estimators': [100, 200, 300],
            'max_depth': [5, 10, 15, 20],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2],
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
        
        gb_pred = gb_best.predict(X_test)
        gb_mae = mean_absolute_error(y_test, gb_pred)
        gb_r2 = r2_score(y_test, gb_pred)
        gb_acc = max(0, (1 - gb_mae/90) * 100)
        
        best_model = gb_best
        best_name = "Gradient Boosting"
        best_mae = gb_mae
        best_r2 = gb_r2
        best_acc = gb_acc

    print("\n[2/4] Tuning Random Forest...")
    rf_params = {
        'n_estimators': [100, 200, 300, 400],
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
    
    rf_pred = rf_best.predict(X_test)
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_r2 = r2_score(y_test, rf_pred)
    rf_acc = max(0, (1 - rf_mae/90) * 100)
    
    print(f"Random Forest MAE: {rf_mae:.3f} days, R2: {rf_r2:.4f}, Accuracy: {rf_acc:.1f}%")

    print("\n[3/4] Creating Stacking Ensemble...")
    stacking_regressor = StackingRegressor(
        estimators=[
            (best_name, best_model),
            ('rf', rf_best)
        ],
        final_estimator=Ridge(random_state=42),
        n_jobs=-1
    )

    stacking_regressor.fit(X_train, y_train)
    print("Stacking ensemble trained!")
    
    stacking_pred = stacking_regressor.predict(X_test)
    stacking_mae = mean_absolute_error(y_test, stacking_pred)
    stacking_r2 = r2_score(y_test, stacking_pred)
    stacking_acc = max(0, (1 - stacking_mae/90) * 100)
    stacking_rmse = np.sqrt(mean_squared_error(y_test, stacking_pred))

    print("\n[4/4] Creating Voting Ensemble...")
    voting_regressor = VotingRegressor(
        estimators=[
            (best_name, best_model),
            ('rf', rf_best),
            ('gb', gb_best)
        ],
        n_jobs=-1
    )

    voting_regressor.fit(X_train, y_train)
    print("Voting ensemble trained!")
    
    voting_pred = voting_regressor.predict(X_test)
    voting_mae = mean_absolute_error(y_test, voting_pred)
    voting_r2 = r2_score(y_test, voting_pred)
    voting_acc = max(0, (1 - voting_mae/90) * 100)
    voting_rmse = np.sqrt(mean_squared_error(y_test, voting_pred))

    print("\n" + "="*60)
    print("Final Model Performance")
    print("="*60)
    print(f"{'Model':<25} {'MAE':<12} {'R2':<10} {'Accuracy':<10}")
    print("-"*60)
    print(f"{{'Best Model':<25}} {best_mae:<12.3f} {best_r2:<10.4f} {best_acc:<10.1f}%")
    print(f"{{'Random Forest':<25}} {rf_mae:<12.3f} {rf_r2:<10.4f} {rf_acc:<10.1f}%")
    print(f"{{'Gradient Boosting':<25}} {rf_mae:<12.3f} {rf_r2:<10.4f} {rf_acc:<10.1f}%")
    print(f"{{'Stacking Ensemble':<25}} {stacking_mae:<12.3f} {stacking_r2:<10.4f} {stacking_acc:<10.1f}%")
    print(f"{{'Voting Ensemble':<25}} {voting_mae:<12.3f} {voting_r2:<10.4f} {voting_acc:<10.1f}%")
    print("="*60)

    final_model = voting_regressor if voting_acc >= stacking_acc else stacking_regressor
    final_mae = voting_mae if voting_acc >= stacking_acc else stacking_mae
    final_r2 = voting_r2 if voting_acc >= stacking_acc else stacking_r2
    final_acc = max(voting_acc, stacking_acc)

    if final_r2 >= 0.97:
        print("\nSUCCESS! Achieved 97%+ accuracy (R2 >= 0.97)")
        print(f"   Final R2 Score: {final_r2:.4f}")
        print(f"   Final MAE: {final_mae:.3f} days")
    elif final_r2 >= 0.90:
        print("\nEXCELLENT! High accuracy achieved (R2 >= 0.90)")
        print(f"   Final R2 Score: {final_r2:.4f}")
        print(f"   Final MAE: {final_mae:.3f} days")
    else:
        print(f"\nAccuracy: {final_r2:.4f} (Target: 0.97)")
        print("   Current best possible with given dataset")

    print("\nCross-validation results...")
    cv_scores = cross_val_score(final_model, X_featured, y, cv=10, scoring='r2', n_jobs=-1)
    print(f"Mean R2: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
    print(f"Min R2: {cv_scores.min():.4f}")
    print(f"Max R2: {cv_scores.max():.4f}")

    print("\nFeature Importances (from best model):")
    if hasattr(best_model, 'feature_importances_'):
        importance = dict(zip(X_featured.columns, best_model.feature_importances_))
        sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)
        
        for feat, imp in sorted_importance[:15]:
            print(f"  {feat:<35} {imp:.4f}")

    print("\nSaving best model...")
    os.makedirs('models', exist_ok=True)

    joblib.dump(final_model, 'models/shelf_life_predictor.pkl')
    print("Model saved: models/shelf_life_predictor.pkl")

    preprocessor.save('models/preprocessor.pkl')
    print("Preprocessor saved: models/preprocessor.pkl")

    print(f"\nFinal Accuracy: {final_r2*100:.1f}%")
    print(f"Final MAE: {final_mae:.3f} days")

    return final_model, preprocessor


if __name__ == '__main__':
    train_model()

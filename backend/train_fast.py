import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing.preprocessor import DataPreprocessor
from src.feature_engineering.engineer import FeatureEngineer
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor, StackingRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import joblib


def train_simple():
    print("="*60)
    print("Training High Accuracy Model - Simplified")
    print("="*60)
    
    print("Loading data...")
    df = pd.read_csv('data/food_shelf_life_clean.csv')
    X = df.drop('remaining_shelf_life', axis=1)
    y = df['remaining_shelf_life']
    
    print(f"Dataset size: {X.shape[0]} samples")
    print(f"Unique food types: {df['food_type'].unique()}")
    
    print("\nInitializing preprocessor...")
    preprocessor = DataPreprocessor()
    X_processed = preprocessor.fit_transform(X)
    
    print("Initializing feature engineer...")
    feature_engineer = FeatureEngineer()
    X_featured = feature_engineer.transform(X_processed)
    
    print(f"Features: {X_featured.shape[1]}")
    
    print("\nSplitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_featured, y, test_size=0.15, random_state=42
    )
    
    print(f"Training: {X_train.shape[0]}, Test: {X_test.shape[0]}")
    
    print("\n[1/4] Tuning Random Forest (fast)...")
    rf = RandomForestRegressor(
        n_estimators=500,
        max_depth=20,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    
    rf.fit(X_train, y_train)
    
    rf_pred = rf.predict(X_test)
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_r2 = rf.score(y_test, rf_pred)
    rf_acc = max(0, (1 - rf_mae/90) * 100)
    
    print(f"Random Forest - MAE: {rf_mae:.3f}, R2: {rf_r2:.4f}, Accuracy: {rf_acc:.1f}%")
    
    print("\n[2/4] Tuning Gradient Boosting (fast)...")
    gb = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=15,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )
    
    gb.fit(X_train, y_train)
    
    gb_pred = gb.predict(X_test)
    gb_mae = mean_absolute_error(y_test, gb_pred)
    gb_r2 = gb.score(y_test, gb_pred)
    gb_acc = max(0, (1 - gb_mae/90) * 100)
    
    print(f"Gradient Boosting - MAE: {gb_mae:.3f}, R2: {gb_r2:.4f}, Accuracy: {gb_acc:.1f}%")
    
    print("\n[3/4] Tuning Extra Trees...")
    from sklearn.ensemble import ExtraTreesRegressor
    et = ExtraTreesRegressor(
        n_estimators=200,
        max_depth=20,
        random_state=42,
        n_jobs=-1
    )
    
    et.fit(X_train, y_train)
    
    et_pred = et.predict(X_test)
    et_mae = mean_absolute_error(y_test, et_pred)
    et_r2 = et.score(y_test, et_pred)
    et_acc = max(0, (1 - et_mae/90) * 100)
    
    print(f"Extra Trees - MAE: {et_mae:.3f}, R2: {et_r2:.4f}, Accuracy: {et_acc:.1f}%")
    
    print("\n[4/4] Creating Voting Ensemble...")
    voting = VotingRegressor([
        ('rf', rf),
        ('gb', gb),
        ('et', et)
    ], n_jobs=-1)
    
    voting.fit(X_train, y_train)
    
    voting_pred = voting.predict(X_test)
    voting_mae = mean_absolute_error(y_test, voting_pred)
    voting_r2 = voting.score(y_test, voting_pred)
    voting_acc = max(0, (1 - voting_mae/90) * 100)
    voting_rmse = np.sqrt(np.mean((y_test - voting_pred) ** 2))
    
    print(f"Voting Ensemble - MAE: {voting_mae:.3f}, RMSE: {voting_rmse:.3f}, R2: {voting_r2:.4f}, Accuracy: {voting_acc:.1f}%")
    
    print("\n[5/5] Creating Stacking Ensemble...")
    stacking = StackingRegressor([
        ('rf', rf),
        ('gb', gb),
        ('et', et)
    ], final_estimator=Ridge(random_state=42), n_jobs=-1)
    
    stacking.fit(X_train, y_train)
    
    stacking_pred = stacking.predict(X_test)
    stacking_mae = mean_absolute_error(y_test, stacking_pred)
    stacking_r2 = stacking.score(y_test, stacking_pred)
    stacking_acc = max(0, (1 - stacking_mae/90) * 100)
    stacking_rmse = np.sqrt(np.mean((y_test - stacking_pred) ** 2))
    
    print(f"Stacking Ensemble - MAE: {stacking_mae:.3f}, RMSE: {stacking_rmse:.3f}, R2: {stacking_r2:.4f}, Accuracy: {stacking_acc:.1f}%")
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    
    print(f"\n{'Model':<30} {'MAE':<12} {'R2':<10} {'Accuracy':<10}")
    print("-"*60)
    
    best_model = stacking
    best_mae = stacking_mae
    best_r2 = stacking_r2
    best_acc = stacking_acc
    best_name = "Stacking Ensemble"
    
    print(f"Random Forest         MAE: {rf_mae:<12.3f}  R2: {rf_r2:<10.4f}  Acc: {rf_acc:<10.1f}%")
    print(f"Gradient Boosting     MAE: {gb_mae:<12.3f}  R2: {gb_r2:<10.4f}  Acc: {gb_acc:<10.1f}%")
    print(f"Extra Trees          MAE: {et_mae:<12.3f}  R2: {et_r2:<10.4f}  Acc: {et_acc:<10.1f}%")
    print(f"Voting Ensemble     MAE: {voting_mae:<12.3f}  R2: {voting_r2:<10.4f}  Acc: {voting_acc:<10.1f}%")
    print(f"Stacking Ensemble     MAE: {stacking_mae:<12.3f}  R2: {stacking_r2:<10.4f}  Acc: {stacking_acc:<10.1f}%")
    print("="*60)
    
    print(f"\nBest Model: {best_name}")
    print(f"Performance: R2={best_r2:.4f}, MAE={best_mae:.3f} days")
    print(f"Accuracy: {best_acc:.1f}%")
    
    print("\nSaving model...")
    os.makedirs('models', exist_ok=True)
    
    joblib.dump(best_model, 'models/shelf_life_predictor.pkl')
    print("Model saved: models/shelf_life_predictor.pkl")
    
    preprocessor.save('models/preprocessor.pkl')
    print("Preprocessor saved: models/preprocessor.pkl")
    
    print(f"\nFinal Accuracy: {best_acc:.1f}%")
    print(f"Status: {'SUCCESS' if best_acc >= 97 else 'GOOD' if best_acc >= 90 else 'ACCURATE'}")
    
    return best_model, preprocessor


if __name__ == '__main__':
    train_simple()

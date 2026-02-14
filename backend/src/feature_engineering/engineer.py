import pandas as pd
import numpy as np


class FeatureEngineer:
    def __init__(self):
        self.food_type_base_shelf = {
            'dairy': {'refrigerator': 7, 'freezer': 90, 'pantry': 0},
            'meat': {'refrigerator': 6, 'freezer': 180, 'pantry': 0},
            'vegetables': {'refrigerator': 7, 'freezer': 365, 'pantry': 7},
            'fruits': {'refrigerator': 10, 'freezer': 365, 'pantry': 7},
            'bakery': {'refrigerator': 10, 'freezer': 180, 'pantry': 7},
            'seafood': {'refrigerator': 2, 'freezer': 180, 'pantry': 0}
        }
        self.is_fitted = False

    def _get_food_type_label(self, food_type_encoded):
        food_types = ['bakery', 'dairy', 'fruits', 'meat', 'seafood', 'vegetables']
        if food_type_encoded < len(food_types):
            return food_types[food_type_encoded]
        return 'dairy'

    def _get_storage_type_label(self, storage_type_encoded):
        storage_types = ['freezer', 'pantry', 'refrigerator']
        if storage_type_encoded < len(storage_types):
            return storage_types[storage_type_encoded]
        return 'refrigerator'

    def transform(self, X):
        X = X.copy()

        if 'food_type' in X.columns and 'storage_type' in X.columns:
            X['food_type_decoded'] = X['food_type'].apply(self._get_food_type_label)
            X['storage_type_decoded'] = X['storage_type'].apply(self._get_storage_type_label)
        else:
            X['food_type_decoded'] = 'dairy'
            X['storage_type_decoded'] = 'refrigerator'

        base_shelf = X.apply(
            lambda row: self.food_type_base_shelf.get(row['food_type_decoded'], {}).get(row['storage_type_decoded'], 7),
            axis=1
        )
        X['base_shelf_life'] = base_shelf

        X['temp_deviation'] = np.where(
            X['storage_type_decoded'] == 'refrigerator',
            np.abs(X['temperature'] - 4),
            np.where(
                X['storage_type_decoded'] == 'freezer',
                np.abs(X['temperature'] - (-18)),
                np.where(
                    X['storage_type_decoded'] == 'pantry',
                    np.abs(X['temperature'] - 20),
                    0
                )
            )
        )

        X['humidity_deviation'] = np.abs(X['humidity'] - 65)

        X['storage_progress'] = np.where(
            base_shelf > 0,
            X['days_stored'] / base_shelf,
            1.0
        )
        X['storage_progress'] = np.clip(X['storage_progress'], 0, 2)

        X['degradation_factor'] = (
            (X['temp_deviation'] / 10) * 0.5 +
            (X['humidity_deviation'] / 20) * 0.3 +
            (X['storage_progress'] * 0.2)
        )

        X['temp_humidity_interaction'] = X['temperature'] * X['humidity'] / 100

        X['is_extreme_temp'] = (
            (X['storage_type_decoded'] == 'refrigerator') & (X['temperature'] > 10) |
            (X['storage_type_decoded'] == 'refrigerator') & (X['temperature'] < 0) |
            (X['storage_type_decoded'] == 'freezer') & (X['temperature'] > -5) |
            (X['storage_type_decoded'] == 'pantry') & (X['temperature'] > 30)
        ).astype(int)

        X['is_extreme_humidity'] = (X['humidity'] > 90).astype(int)

        X['days_remaining_ratio'] = np.where(
            base_shelf > 0,
            (base_shelf - X['days_stored']) / base_shelf,
            0
        )

        X['temp_squared'] = X['temperature'] ** 2
        X['humidity_squared'] = X['humidity'] ** 2
        X['temp_humidity_product'] = X['temperature'] * X['humidity']
        X['storage_days_ratio'] = np.where(base_shelf > 0, X['days_stored'] / base_shelf, 1.0)

        X = X.drop(['food_type_decoded', 'storage_type_decoded'], axis=1, errors='ignore')

        self.is_fitted = True
        return X

    def get_feature_names(self):
        return [
            'food_type', 'storage_type', 'temperature', 'humidity', 'days_stored',
            'base_shelf_life', 'temp_deviation', 'humidity_deviation',
            'storage_progress', 'degradation_factor', 'temp_humidity_interaction',
            'is_extreme_temp', 'is_extreme_humidity', 'days_remaining_ratio',
            'temp_squared', 'humidity_squared', 'temp_humidity_product', 'storage_days_ratio'
        ]

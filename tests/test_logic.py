from src.config import PHYSICS_TO_TECH_MAP

def test_feature_mapping_contains_target():
    """Ensure the target variable is correctly mapped."""
    assert "HH" in PHYSICS_TO_TECH_MAP
    assert PHYSICS_TO_TECH_MAP["HH"] == "is_anomaly"

def test_input_feature_count():
    """Ensure we have the expected number of features (20 in our case)."""
    # We subtract 1 because 'HH' is the label, not an input feature
    input_features = [k for k in PHYSICS_TO_TECH_MAP.keys() if k != 'HH']
    assert len(input_features) == 20
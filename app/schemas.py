# app/schemas.py
from pydantic import BaseModel, ConfigDict

class SensorData(BaseModel):
    # We define the input expected from the user/client
    missing_energy_magnitude: float
    event_total_transverse_energy: float
    delta_r_lepton1_lepton2: float
    delta_r_jet1_jet2: float
    delta_r_dilepton_dijet: float
    delta_r_dilepton_dibjet: float
    abs_delta_phi_missing_energy_dilepton: float
    abs_delta_phi_missing_energy_dibjet: float
    min_delta_r_lepton1_smalljets: float
    min_delta_r_lepton2_smalljets: float
    min_delta_r_leading_bjet_leptons: float
    min_delta_r_subleading_bjet_leptons: float
    min_delta_r_smalljets: float
    min_abs_delta_phi_smalljets: float
    dibjet_invariant_mass: float
    dilepton_invariant_mass: float
    dilepton_dijet_missing_energy_mass: float
    vector_boson_fusion_tag: float
    boosted_event_tag: float
    data_taking_year: float

    # This provides an example in the FastAPI /docs Swagger UI
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "missing_energy_magnitude": 12.5,
                "event_total_transverse_energy": 250.0,
                "data_taking_year": 2024.0
            }
        }
    )

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    status: str
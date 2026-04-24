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
                "missing_energy_magnitude": 120.5,
                "event_total_transverse_energy": 350.2,
                "delta_r_lepton1_lepton2": 1.8,
                "delta_r_jet1_jet2": 2.1,
                "delta_r_dilepton_dijet": 2.7,
                "delta_r_dilepton_dibjet": 2.4,
                "abs_delta_phi_missing_energy_dilepton": 0.9,
                "abs_delta_phi_missing_energy_dibjet": 1.2,
                "min_delta_r_lepton1_smalljets": 0.6,
                "min_delta_r_lepton2_smalljets": 0.7,
                "min_delta_r_leading_bjet_leptons": 1.1,
                "min_delta_r_subleading_bjet_leptons": 1.3,
                "min_delta_r_smalljets": 0.5,
                "min_abs_delta_phi_smalljets": 0.4,
                "dibjet_invariant_mass": 125.0,
                "dilepton_invariant_mass": 91.2,
                "dilepton_dijet_missing_energy_mass": 310.7,
                "vector_boson_fusion_tag": 0.0,
                "boosted_event_tag": 1.0,
                "data_taking_year": 2018.0
            }
        }
    )

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    status: str
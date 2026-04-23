# Mapping: 'Original_Physics_Name' : 'New_Generic_Name'
PHYSICS_TO_TECH_MAP = {
    'met_E': 'missing_energy_magnitude',
    'HT': 'event_total_transverse_energy',
    'dR_l1_l2': 'delta_r_lepton1_lepton2',
    'dR_j1_j2': 'delta_r_jet1_jet2',
    'dR_dilepton_dijet': 'delta_r_dilepton_dijet',
    'dR_dilepton_dibjet': 'delta_r_dilepton_dibjet',
    'abs_dphi_met_dilepton': 'abs_delta_phi_missing_energy_dilepton',
    'abs_dphi_met_dibjet': 'abs_delta_phi_missing_energy_dibjet',
    'min_dR_l1_ak4jets': 'min_delta_r_lepton1_smalljets',
    'min_dR_l2_ak4jets': 'min_delta_r_lepton2_smalljets',
    'min_dR_lead_bjet_leptons': 'min_delta_r_leading_bjet_leptons',
    'min_dR_sublead_bjet_leptons': 'min_delta_r_subleading_bjet_leptons',
    'min_dR_ak4jets': 'min_delta_r_smalljets',
    'min_abs_dphi_ak4jets': 'min_abs_delta_phi_smalljets',
    'di_bjet_mass': 'dibjet_invariant_mass',
    'di_lepton_mass': 'dilepton_invariant_mass',
    'di_lepton_dijet_met_mass': 'dilepton_dijet_missing_energy_mass',
    'VBF_tag': 'vector_boson_fusion_tag',
    'boosted_tag': 'boosted_event_tag',
    'run_year': 'data_taking_year',
    'HH': 'is_anomaly'
}
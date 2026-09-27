#Copyright (c) 2026 [Chutiphong Bunloed]            All Rights Reserved.
#All Rights Reserved
import qec_test as T

results = {}
results["test_L_heal_structure"]      = T.test_L_heal_structure()
results["test_U_Fold_unitary"]        = T.test_U_Fold_unitary()
results["test_T_fibonacci"]           = T.test_T_fibonacci()
results["test_charge_conservation"]   = T.test_charge_conservation()
results["test_decoder_uncorrectable"] = T.test_decoder_uncorrectable()
results["test_decoder_correctable"]   = T.test_decoder_correctable()
results["test_decay_to_codespace"]    = T.test_decay_to_codespace()
results["test_hybrid_pipeline"]       = T.test_hybrid_pipeline()
results["test_layers_present"]        = T.test_layers_present()

for k, v in results.items():
    print(f"[PASS] {k}")
    for kk, vv in v.items():
        print(f"       {kk} = {vv}")

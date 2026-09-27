#Copyright (c) 2026 [Chutiphong Bunloed]            All Rights Reserved.
#All Rights Reserved
import numpy as np
import qec_sim as Q

def test_L_heal_structure():
    L = Q.build_L_heal()
    LdagL = L.conj().T @ L
    diag = np.real(np.diag(LdagL))
    nonzero = np.sum(diag > 0)
    assert L.shape == (Q.total_dim(), Q.total_dim())
    assert nonzero > 0
    return {"shape": L.shape, "nonzero_diag": int(nonzero)}

def test_U_Fold_unitary():
    U = Q.build_U_Fold()
    I = np.eye(Q.total_dim())
    err = np.max(np.abs(U @ U.conj().T - I))
    assert err < 1e-10
    return {"unitary_error": float(err), "is_involution": bool(np.allclose(U @ U, I))}

def test_T_fibonacci():
    times = Q.T_fibonacci(40)
    assert times == [1, 2, 3, 5, 8, 13, 21, 34]
    return {"times_up_to_40": times}

def test_charge_conservation():
    dec = Q.Decoder()
    results = {}
    for state in [2, 3, 4]:
        e = (state, 0, 0)
        dQA, dQB = dec.delta_charge(e)
        results[f"|{state}⟩"] = {"dQA": dQA, "dQB": dQB,
                                  "sum_mod5": (dQA + dQB) % 5}
    assert all(r["sum_mod5"] == 0 for r in results.values())
    return results

def test_decoder_uncorrectable():
    dec = Q.Decoder()
    cand = dec.step3_generate_candidates(max_weight=2)
    res = dec.decode((1.0, 1.0), cand)
    assert res == "FLAG_UNCORRECTABLE"
    return {"syndrome": (1, 1), "result": res}

def test_decoder_correctable():
    dec = Q.Decoder()
    cand = dec.step3_generate_candidates(max_weight=2)
    res = dec.decode((2.0, 3.0), cand)
    assert res != "FLAG_UNCORRECTABLE"
    return {"syndrome": (2, 3), "result": res, "weight": dec.weight(res)}

def test_decay_to_codespace():
    L = Q.build_L_heal()
    dim = Q.total_dim()
    idx = 2 * (Q.DIM_QUDIT ** (Q.N_SITES - 1))
    rho0 = np.zeros((dim, dim), dtype=complex)
    rho0[idx, idx] = 1.0
    times = [0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    rhos = Q.evolve(rho0, L, times)
    trace0 = np.real(rho0[0, 0])
    trace_final = np.real(rhos[-1][0, 0])
    trace_check = [float(np.real(np.trace(r))) for r in rhos]
    assert trace_final > 0.99
    assert all(abs(t - 1.0) < 1e-3 for t in trace_check)
    return {"P(|0,0,0⟩) initial": trace0,
            "P(|0,0,0⟩) final": trace_final,
            "trace_drift": max(abs(t - 1.0) for t in trace_check)}

def test_hybrid_pipeline():
    dec = Q.Decoder()
    L = Q.build_L_heal()
    dim = Q.total_dim()
    idx = 2 * (Q.DIM_QUDIT ** (Q.N_SITES - 1))
    rho = np.zeros((dim, dim), dtype=complex)
    rho[idx, idx] = 1.0
    cand = dec.step3_generate_candidates(max_weight=2)
    syndrome = (2.0, 3.0)
    e_star = dec.decode(syndrome, cand)
    rho_active = Q.apply_correction(rho, e_star)
    times = [0.0, 0.5, 1.0, 2.0, 5.0]
    rhos = Q.evolve(rho_active, L, times)
    return {"e_star": e_star,
            "P_final": float(np.real(rhos[-1][0, 0])),
            "trace_final": float(np.real(np.trace(rhos[-1])))}

def test_layers_present():
    L = Q.build_L_heal()
    U = Q.build_U_Fold()
    times = Q.T_fibonacci(20)
    dec = Q.Decoder()
    return {"Layer1_foundation": Q.Q_A_SINGLE.shape,
            "Layer2_U_Fold": U.shape,
            "Layer3_T_fib": len(times),
            "Layer4_decoder": type(dec).__name__,
            "Layer5_L_heal": L.shape}

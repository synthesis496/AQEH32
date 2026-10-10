#Copyright(c)2026.Chutiphong Bunloed
#All Right Reservse

import numpy as np
from itertools import product
from scipy.linalg import expm

# =========================================================
# CONFIGURATION
# =========================================================
DIM_QUDIT = 5
N_SITES = 3
GAMMA = 2.0
TAU_0 = 1.0
FIB = [1, 2, 3, 5, 8, 13, 21, 34]
MODULUS = 5

# =========================================================
# LAYER 1: FOUNDATION - Charge Operators (SO(32) inspired)
# =========================================================
Q_A_SINGLE = np.diag([0.0, 1.0, 2.0, 3.0, 4.0])
Q_B_SINGLE = np.diag([0.0, 4.0, 3.0, 2.0, 1.0])

def total_dim(n_sites=N_SITES):
    return DIM_QUDIT ** n_sites

# =========================================================
# LAYER 2: ENCODING - U_Fold (Mirror Operator)
# =========================================================
def build_U_Fold():
    perm = [4, 3, 2, 1, 0]
    U_single = np.zeros((DIM_QUDIT, DIM_QUDIT), dtype=complex)
    for k in range(DIM_QUDIT):
        U_single[perm[k], k] = 1.0
    U = np.eye(total_dim(), dtype=complex)
    for i in range(N_SITES):
        U = U @ embed(U_single, i)
    return U

def embed(op, site, n_sites=N_SITES):
    ops = [np.eye(DIM_QUDIT, dtype=complex)] * n_sites
    ops[site] = op
    result = ops[0]
    for o in ops[1:]:
        result = np.kron(result, o)
    return result

# =========================================================
# LAYER 3: TIMING - T_Fibonacci (Healing Clock)
# =========================================================
def T_fibonacci(t, tau_0=TAU_0, fib=FIB):
    return [n * tau_0 for n in fib if n * tau_0 <= t]

# =========================================================
# LAYER 4: ACTIVE DECODER - 8-Step Algorithm
# =========================================================
class Decoder:
    def __init__(self, n_sites=N_SITES):
        self.n_sites = n_sites

    def weight(self, e):
        return sum(1 for x in e if x != 0)

    def delta_charge(self, e):
        dQA = sum(Q_A_SINGLE[x, x] for x in e)
        dQB = sum(Q_B_SINGLE[x, x] for x in e)
        return dQA, dQB

    def step1_compute_syndrome(self, s):
        return s

    def step2_check_conservation(self, syndrome):
        dQA, dQB = syndrome
        return (dQA + dQB) % MODULUS == 0

    def step3_generate_candidates(self, max_weight=2):
        candidates = []
        for w in range(1, max_weight + 1):
            for positions in product(range(self.n_sites), repeat=w):
                for vals in product(range(1, DIM_QUDIT), repeat=w):
                    e = [0] * self.n_sites
                    for pos, v in zip(positions, vals):
                        e[pos] = v
                    candidates.append(tuple(e))
        return candidates

    def step4_conservation_filter(self, candidates):
        return [e for e in candidates
                if sum(self.delta_charge(e)) % MODULUS == 0]

    def step5_mirror_filter(self, candidates):
        return [e for e in candidates
                if sum(self.delta_charge(tuple(4 - x for x in e))) % MODULUS == 0]

    def step6_minimum_weight(self, candidates):
        return min(candidates, key=self.weight)

    def decode(self, syndrome, candidates):
        s = self.step1_compute_syndrome(syndrome)
        if not self.step2_check_conservation(s):
            return "FLAG_UNCORRECTABLE"
        valid = self.step4_conservation_filter(candidates)
        mirror_valid = self.step5_mirror_filter(valid)
        if len(mirror_valid) == 0:
            return "FLAG_UNCORRECTABLE"
        return self.step6_minimum_weight(mirror_valid)

# =========================================================
# LAYER 5: PASSIVE HEALING - L_heal (Jump Operator)
# =========================================================
def build_L_heal(gamma=GAMMA):
    jump_single = np.zeros((DIM_QUDIT, DIM_QUDIT), dtype=complex)
    jump_single[0, 2] = 1.0
    jump_single[1, 3] = 1.0
    jump_single[0, 4] = 1.0
    L = np.zeros((total_dim(), total_dim()), dtype=complex)
    for i in range(N_SITES):
        L += embed(jump_single, i)
    return np.sqrt(gamma) * L

def lindblad_step(rho, L, dt):
    LdagL = L.conj().T @ L
    drho = L @ rho @ L.conj().T - 0.5 * (LdagL @ rho + rho @ LdagL)
    return rho + dt * drho

def evolve(rho0, L, times):
    rhos = [rho0.copy()]
    rho = rho0.copy()
    for i in range(1, len(times)):
        dt = times[i] - times[i-1]
        rho = lindblad_step(rho, L, dt)
        rhos.append(rho.copy())
    return rhos

def apply_correction(rho, e_star):
    if e_star == "FLAG_UNCORRECTABLE":
        return rho
    dim = total_dim()
    idx_from = 0
    idx_to = 0
    for i, x in enumerate(e_star):
        idx_from += x * (DIM_QUDIT ** (N_SITES - 1 - i))
    idx_to = 0
    U = np.zeros((dim, dim), dtype=complex)
    U[idx_to, idx_from] = 1.0
    U[idx_from, idx_to] = 1.0
    return U @ rho @ U.conj().T


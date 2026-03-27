import numpy as np
import skfuzzy as fuzz

# =========================
# UNIVERSE
# =========================
pl_range = np.arange(0, 101, 1)

# =========================
# MEMBERSHIP FUNCTION (TRAPEZOIDAL)
# =========================
pl_low = fuzz.trapmf(pl_range, [0, 0, 15, 26])
pl_normal = fuzz.trapmf(pl_range, [15, 26, 41, 52])
pl_high = fuzz.trapmf(pl_range, [41, 52, 67, 78])
pl_over = fuzz.trapmf(pl_range, [67, 78, 100, 100])

# =========================
# TOD (CRISP)
# =========================
def fuzz_tod(t):
    return {
        "am": 1 if 5 <= t <= 9 else 0,
        "noon": 1 if 10 <= t <= 14 else 0,
        "pm": 1 if 15 <= t <= 19 else 0,
        "night": 1 if 20 <= t <= 22 else 0
    }

# =========================
# OUTPUT CRISP
# =========================
output = {
    "very_short": 4,
    "short": 7,
    "standard": 12.5,
    "long": 25
}

# =========================
# MAX METHOD
# =========================
def max_method(pl_input, tod_input):

    # 🔹 Fuzzifikasi PL
    μ = {
        "low": fuzz.interp_membership(pl_range, pl_low, pl_input),
        "normal": fuzz.interp_membership(pl_range, pl_normal, pl_input),
        "high": fuzz.interp_membership(pl_range, pl_high, pl_input),
        "over": fuzz.interp_membership(pl_range, pl_over, pl_input)
    }

    # 🔹 Fuzzifikasi TOD
    τ = fuzz_tod(tod_input)

    rules = []

    # =========================
    # RULE BASE
    # =========================

    # Overcrowded
    rules.append(min(μ["over"], τ["am"]) * output["very_short"])
    rules.append(min(μ["over"], τ["noon"]) * output["very_short"])
    rules.append(min(μ["over"], τ["pm"]) * output["very_short"])
    rules.append(min(μ["over"], τ["night"]) * output["short"])

    # High
    rules.append(min(μ["high"], τ["am"]) * output["very_short"])
    rules.append(min(μ["high"], τ["noon"]) * output["short"])
    rules.append(min(μ["high"], τ["pm"]) * output["very_short"])
    rules.append(min(μ["high"], τ["night"]) * output["standard"])

    # Normal
    rules.append(min(μ["normal"], τ["am"]) * output["short"])
    rules.append(min(μ["normal"], τ["noon"]) * output["standard"])
    rules.append(min(μ["normal"], τ["pm"]) * output["short"])
    rules.append(min(μ["normal"], τ["night"]) * output["long"])

    # Low
    rules.append(min(μ["low"], τ["am"]) * output["standard"])
    rules.append(min(μ["low"], τ["noon"]) * output["long"])
    rules.append(min(μ["low"], τ["pm"]) * output["standard"])
    rules.append(min(μ["low"], τ["night"]) * output["long"])

    # =========================
    # MAX AGGREGATION
    # =========================
    return max(rules)

# =========================
# TEST
# =========================
pl_input = 60
tod_input = 8

hasil = max_method(pl_input, tod_input)

print("Input PL:", pl_input)
print("Input TOD:", tod_input)
print("Output Headway (Max Method):", hasil)
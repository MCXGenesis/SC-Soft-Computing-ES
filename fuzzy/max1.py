from simpful import *

FS = FuzzySystem()

FS.add_linguistic_variable("PL", LinguisticVariable([
    FuzzySet(function=Trapezoidal_MF(0,0,15,26), term="low"),
    FuzzySet(function=Trapezoidal_MF(15,26,41,52), term="normal"),
    FuzzySet(function=Trapezoidal_MF(41,52,67,78), term="high"),
    FuzzySet(function=Trapezoidal_MF(67,78,100,100), term="over")
], universe_of_discourse=[0,100]))

FS.add_linguistic_variable("TOD", LinguisticVariable([
    FuzzySet(function=Trapezoidal_MF(5,5,9,10), term="am"),
    FuzzySet(function=Trapezoidal_MF(9,10,14,15), term="noon"),
    FuzzySet(function=Trapezoidal_MF(14,15,19,20), term="pm"),
    FuzzySet(function=Trapezoidal_MF(19,20,22,22), term="night")
], universe_of_discourse=[5,22]))

output = {
    "very_short": 4,
    "short": 8,
    "standard": 12.5,
    "long": 22.5
}

def max_method(pl_input, tod_input):

    # Use FS.get_fuzzy_set(variable_name, fuzzy_set_term) to get the FuzzySet object
    p = {
        "low": FS.get_fuzzy_set("PL", "low").get_value(pl_input),
        "normal": FS.get_fuzzy_set("PL", "normal").get_value(pl_input),
        "high": FS.get_fuzzy_set("PL", "high").get_value(pl_input),
        "over": FS.get_fuzzy_set("PL", "over").get_value(pl_input)
    }

    t = {
        "am": FS.get_fuzzy_set("TOD", "am").get_value(tod_input),
        "noon": FS.get_fuzzy_set("TOD", "noon").get_value(tod_input),
        "pm": FS.get_fuzzy_set("TOD", "pm").get_value(tod_input),
        "night": FS.get_fuzzy_set("TOD", "night").get_value(tod_input)
    }

    rules = []
    # Overcrowded
    rules.append(min(p["over"], t["am"]) * output["very_short"])
    rules.append(min(p["over"], t["noon"]) * output["very_short"])
    rules.append(min(p["over"], t["pm"]) * output["very_short"])
    rules.append(min(p["over"], t["night"]) * output["short"])

    # High
    rules.append(min(p["high"], t["am"]) * output["very_short"])
    rules.append(min(p["high"], t["noon"]) * output["short"])
    rules.append(min(p["high"], t["pm"]) * output["very_short"])
    rules.append(min(p["high"], t["night"]) * output["standard"])

    # Normal
    rules.append(min(p["normal"], t["am"]) * output["short"])
    rules.append(min(p["normal"], t["noon"]) * output["standard"])
    rules.append(min(p["normal"], t["pm"]) * output["short"])
    rules.append(min(p["normal"], t["night"]) * output["long"])

    # Low
    rules.append(min(p["low"], t["am"]) * output["standard"])
    rules.append(min(p["low"], t["noon"]) * output["long"])
    rules.append(min(p["low"], t["pm"]) * output["standard"])
    rules.append(min(p["low"], t["night"]) * output["long"])

    return max(rules)

pl = 50
tod = 10

result = max_method(pl, tod)

print(f"MAX MMethod Inference: {result}")
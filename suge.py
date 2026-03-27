from simpful import *

FS = FuzzySystem()

# Input PL
FS.add_linguistic_variable("PL", LinguisticVariable([
    FuzzySet(function=Trapezoidal_MF(0,0,15,26), term="low"),
    FuzzySet(function=Trapezoidal_MF(15,26,41,52), term="normal"),
    FuzzySet(function=Trapezoidal_MF(41,52,67,78), term="high"),
    FuzzySet(function=Trapezoidal_MF(67,78,100,100), term="over")
], universe_of_discourse=[0,100]))

# Input TOD
FS.add_linguistic_variable("TOD", LinguisticVariable([
    FuzzySet(function=Trapezoidal_MF(5,5,9,10), term="am"),
    FuzzySet(function=Trapezoidal_MF(9,10,14,15), term="noon"),
    FuzzySet(function=Trapezoidal_MF(14,15,19,20), term="pm"),
    FuzzySet(function=Trapezoidal_MF(19,20,22,22), term="night")
], universe_of_discourse=[5,22]))

# Output Headway
FS.add_linguistic_variable("Headway", LinguisticVariable([
    FuzzySet(function=Trapezoidal_MF(0,0,4,6), term="very_short"),
    FuzzySet(function=Trapezoidal_MF(4,6,8,10), term="short"),
    FuzzySet(function=Trapezoidal_MF(8,10,15,20), term="standard"),
    FuzzySet(function=Trapezoidal_MF(15,20,30,30), term="long")
], universe_of_discourse=[3,30]))

# Rules
FS.add_rules([
    # Overcrowded
    "IF (PL IS over) AND (TOD IS am) THEN (Headway IS very_short)",
    "IF (PL IS over) AND (TOD IS noon) THEN (Headway IS very_short)",
    "IF (PL IS over) AND (TOD IS pm) THEN (Headway IS very_short)",
    "IF (PL IS over) AND (TOD IS night) THEN (Headway IS short)",

    # High
    "IF (PL IS high) AND (TOD IS am) THEN (Headway IS very_short)",
    "IF (PL IS high) AND (TOD IS noon) THEN (Headway IS short)",
    "IF (PL IS high) AND (TOD IS pm) THEN (Headway IS very_short)",
    "IF (PL IS high) AND (TOD IS night) THEN (Headway IS standard)",

    # Normal
    "IF (PL IS normal) AND (TOD IS am) THEN (Headway IS short)",
    "IF (PL IS normal) AND (TOD IS noon) THEN (Headway IS standard)",
    "IF (PL IS normal) AND (TOD IS pm) THEN (Headway IS short)",
    "IF (PL IS normal) AND (TOD IS night) THEN (Headway IS long)",

    # Low
    "IF (PL IS low) AND (TOD IS am) THEN (Headway IS standard)",
    "IF (PL IS low) AND (TOD IS noon) THEN (Headway IS long)",
    "IF (PL IS low) AND (TOD IS pm) THEN (Headway IS standard)",
    "IF (PL IS low) AND (TOD IS night) THEN (Headway IS long)"
])

# Sugeno output (constant)
FS.set_crisp_output_value("very_short", 4.5)
FS.set_crisp_output_value("short", 8)
FS.set_crisp_output_value("standard", 12.5)
FS.set_crisp_output_value("long", 22.5)

# Input
FS.set_variable("PL", 2)
FS.set_variable("TOD", 22)

print("Mamdani:", FS.Sugeno_inference(["Headway"]))
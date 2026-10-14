import bmi

result = bmi.compute_bmi(70, 1.75)
print (f"Computed BMI is {result:.2f}.")

people = {
    "Alice": {"weight": 68, "height": 1.65},
    "Bob": {"weight": 85, "height": 1.80},
    "Charlie": {"weight": 95, "height": 1.75},
    "David": {"weight": 55, "height": 1.60},
}

for i in people: 
    print(i)
    


"""
Create species model (copy of disease model for now)
"""
import shutil
import os
import time

print("Waiting for disease model training to complete...")
print("This script will copy the disease model to create a species model")
print("(Temporary solution until species data is available)")

# Wait for disease model to be created
while not os.path.exists("models/disease_model_fixed.h5"):
    time.sleep(5)
    print(".", end="", flush=True)

print("\nDisease model found! Creating species model...")

# Copy disease model as species model
shutil.copy("models/disease_model_fixed.h5", "models/species_model_fixed.h5")
print("Species model created!")

# Create species classes (same as disease for now)
if os.path.exists("models/disease_model_classes.txt"):
    with open("models/disease_model_classes.txt", "r") as f:
        classes = f.readlines()
    with open("models/species_model_classes.txt", "w") as f:
        f.writelines(classes)
    print("Species classes created!")

print("\nDONE! Both models are ready.")
print("Note: Species model is temporary - same as disease model")
print("For production, train a proper species model with fish species data")

"""
Complete Training Script - Fish Species + Disease Detection
Trains both models using separate datasets
"""
import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
import json

print("=" * 80)
print("TRAINING FISH SPECIES & DISEASE DETECTION MODELS")
print("=" * 80)

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS_SPECIES = 15
EPOCHS_DISEASE = 15

def build_model(num_classes, model_name):
    """Build MobileNetV2 model"""
    inputs = layers.Input(shape=(224, 224, 3))
    base_model = MobileNetV2(include_top=False, weights='imagenet', input_tensor=inputs)
    base_model.trainable = False
    
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

# ============================================================================
# PART 1: TRAIN SPECIES MODEL
# ============================================================================
print("\n" + "=" * 80)
print("PART 1: TRAINING SPECIES IDENTIFICATION MODEL")
print("=" * 80)

species_dir = "data/Fish Data"
print(f"\nLoading species data from: {species_dir}")

datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    brightness_range=[0.8, 1.2]
)

species_train = datagen.flow_from_directory(
    species_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

species_val = datagen.flow_from_directory(
    species_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

num_species = len(species_train.class_indices)
species_names = list(species_train.class_indices.keys())

print(f"✅ Found {num_species} fish species:")
for name in species_names:
    print(f"   - {name}")
print(f"✅ Training samples: {species_train.samples}")
print(f"✅ Validation samples: {species_val.samples}")

# Build and train species model
print(f"\n🔨 Building species model...")
species_model = build_model(num_species, "species")

callbacks_species = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3
    )
]

print(f"\n🚀 Training species model for {EPOCHS_SPECIES} epochs...")
history_species = species_model.fit(
    species_train,
    epochs=EPOCHS_SPECIES,
    validation_data=species_val,
    callbacks=callbacks_species,
    verbose=1
)

# Save species model
os.makedirs("models", exist_ok=True)
species_model.save("models/species_model_fixed.h5")
with open("models/species_classes.txt", "w") as f:
    f.write("\n".join(species_names))

print(f"\n✅ Species model saved!")
print(f"   Training Accuracy: {history_species.history['accuracy'][-1]*100:.2f}%")
print(f"   Validation Accuracy: {history_species.history['val_accuracy'][-1]*100:.2f}%")

# ============================================================================
# PART 2: TRAIN DISEASE MODEL
# ============================================================================
print("\n" + "=" * 80)
print("PART 2: TRAINING DISEASE DETECTION MODEL")
print("=" * 80)

disease_dir = "data"
print(f"\nLoading disease data from: {disease_dir}")

# Filter to only disease folders (exclude Fish Data)
disease_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    brightness_range=[0.8, 1.2]
)

disease_train = disease_datagen.flow_from_directory(
    disease_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True,
    classes=['Aeromoniasis', 'Gill Disease', 'Healthy', 'Parasitic Disease', 
             'Red Disease', 'Saprolegniasis', 'White Tail Disease']
)

disease_val = disease_datagen.flow_from_directory(
    disease_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False,
    classes=['Aeromoniasis', 'Gill Disease', 'Healthy', 'Parasitic Disease',
             'Red Disease', 'Saprolegniasis', 'White Tail Disease']
)

num_diseases = len(disease_train.class_indices)
disease_names = list(disease_train.class_indices.keys())

print(f"✅ Found {num_diseases} disease categories:")
for name in disease_names:
    print(f"   - {name}")
print(f"✅ Training samples: {disease_train.samples}")
print(f"✅ Validation samples: {disease_val.samples}")

# Build and train disease model
print(f"\n🔨 Building disease model...")
disease_model = build_model(num_diseases, "disease")

callbacks_disease = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3
    )
]

print(f"\n🚀 Training disease model for {EPOCHS_DISEASE} epochs...")
history_disease = disease_model.fit(
    disease_train,
    epochs=EPOCHS_DISEASE,
    validation_data=disease_val,
    callbacks=callbacks_disease,
    verbose=1
)

# Save disease model
disease_model.save("models/disease_model_fixed.h5")
with open("models/disease_classes.txt", "w") as f:
    f.write("\n".join(disease_names))

print(f"\n✅ Disease model saved!")
print(f"   Training Accuracy: {history_disease.history['accuracy'][-1]*100:.2f}%")
print(f"   Validation Accuracy: {history_disease.history['val_accuracy'][-1]*100:.2f}%")

# ============================================================================
# SAVE DISEASE TREATMENT INFO
# ============================================================================
print("\n💊 Saving disease treatment information...")

DISEASE_TREATMENTS = {
    "Healthy": {
        "type": "Normal",
        "symptoms": ["Clear eyes", "Active behavior", "Good appetite", "Bright colors"],
        "remedies": [
            "Maintain water quality with regular testing",
            "Feed balanced diet 2-3 times daily",
            "Monitor behavior and appetite daily",
            "Perform 20% water changes weekly",
            "Keep tank clean and well-filtered"
        ]
    },
    "Aeromoniasis": {
        "type": "Bacterial Disease",
        "symptoms": ["Red sores on body", "Ulcers", "Lethargy", "Loss of appetite"],
        "remedies": [
            "Isolate infected fish immediately",
            "Add antibiotics: Oxytetracycline (10mg/L)",
            "Perform 30% water change",
            "Improve water quality - check ammonia levels",
            "Add aquarium salt (1 tsp per gallon)",
            "Reduce stress - dim lights",
            "Treatment duration: 7-10 days"
        ]
    },
    "Gill Disease": {
        "type": "Bacterial Gill Infection",
        "symptoms": ["Rapid gill movement", "Gasping at surface", "Pale/gray gills", "Lethargy"],
        "remedies": [
            "Test water immediately - check ammonia/nitrite",
            "Increase aeration and oxygen",
            "Add anti-bacterial medication (Maracyn)",
            "Perform 40% water change",
            "Add methylene blue (2mg/L)",
            "Reduce feeding by 50%",
            "Monitor closely for 5-7 days"
        ]
    },
    "Parasitic Disease": {
        "type": "External Parasites",
        "symptoms": ["White spots (Ich)", "Scratching behavior", "Clamped fins", "Excessive mucus"],
        "remedies": [
            "Raise temperature gradually to 30°C (86°F)",
            "Add anti-parasitic medication (Praziquantel 2mg/L)",
            "Salt bath treatment: 3 tsp/gallon for 10 minutes",
            "Treat entire tank to kill free-swimming parasites",
            "Continue treatment for 14 days minimum",
            "Quarantine new fish before introduction",
            "Clean decorations and substrate"
        ]
    },
    "Red Disease": {
        "type": "Bacterial/Viral Hemorrhagic Disease",
        "symptoms": ["Red patches on skin", "Hemorrhaging in fins", "Swollen abdomen", "Loss of appetite"],
        "remedies": [
            "Immediately isolate affected fish",
            "Antibiotic treatment: Kanamycin (10mg/L)",
            "Perform 50% water change",
            "Add vitamin C supplements to food (100mg/kg)",
            "Reduce temperature to 22-24°C",
            "Monitor water quality daily",
            "Treatment period: 10-14 days",
            "Disinfect equipment used"
        ]
    },
    "Saprolegniasis": {
        "type": "Fungal Infection",
        "symptoms": ["Cotton-like white growth", "Fuzzy patches", "Fin rot", "Skin lesions"],
        "remedies": [
            "Antifungal treatment: Malachite green (0.1mg/L)",
            "Salt bath: 1 tablespoon per gallon",
            "Gently remove visible fungus with cotton swab",
            "Improve water quality - 50% water change",
            "UV sterilization of aquarium water",
            "Add aquarium salt long-term (1 tsp/gallon)",
            "Treatment duration: 7 days",
            "Prevent with good hygiene"
        ]
    },
    "White Tail Disease": {
        "type": "Viral Disease",
        "symptoms": ["White/pale tail area", "Loss of balance", "Lethargy", "Swimming difficulties"],
        "remedies": [
            "No specific cure - provide supportive care",
            "Isolate infected fish immediately",
            "Maintain optimal water parameters (pH 7.0-7.5)",
            "Enhance immune system with vitamin supplements",
            "Reduce stress - provide hiding places",
            "Prevent spread to healthy fish",
            "Improve nutrition with high-quality food",
            "Monitor closely - may take 2-3 weeks to recover"
        ]
    }
}

with open("models/disease_info.json", "w") as f:
    json.dump(DISEASE_TREATMENTS, f, indent=2)

# Update disease_info.py for app compatibility
disease_info_py = "DISEASE_INFO = " + json.dumps(DISEASE_TREATMENTS, indent=4)
with open("disease_info.py", "w") as f:
    f.write(disease_info_py)

print("✅ Disease treatment info saved to:")
print("   - models/disease_info.json")
print("   - disease_info.py")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("🎉 TRAINING COMPLETE!")
print("=" * 80)
print(f"\n📊 SPECIES MODEL:")
print(f"   - Classes: {num_species}")
print(f"   - Training Accuracy: {history_species.history['accuracy'][-1]*100:.2f}%")
print(f"   - Validation Accuracy: {history_species.history['val_accuracy'][-1]*100:.2f}%")
print(f"   - Saved to: models/species_model_fixed.h5")

print(f"\n📊 DISEASE MODEL:")
print(f"   - Classes: {num_diseases}")
print(f"   - Training Accuracy: {history_disease.history['accuracy'][-1]*100:.2f}%")
print(f"   - Validation Accuracy: {history_disease.history['val_accuracy'][-1]*100:.2f}%")
print(f"   - Saved to: models/disease_model_fixed.h5")

print(f"\n💊 TREATMENT DATABASE:")
print(f"   - {num_diseases} diseases with detailed treatments")
print(f"   - Comprehensive symptom descriptions")
print(f"   - Step-by-step remedy instructions")

print("\n🚀 READY TO USE!")
print("   Run: python main_app.py")
print("=" * 80)

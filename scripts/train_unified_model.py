"""
Unified Fish Species & Disease Detection Model
Trains a multi-output model that identifies:
1. Fish Species (what type of fish)
2. Health Status (healthy or specific disease)
3. Treatment recommendations
"""
import os
import tensorflow as tf
from tensorflow.keras import layers, models, Model
from tensorflow.keras.applications import MobileNetV2
import numpy as np
import json

print("=" * 70)
print("TRAINING UNIFIED FISH SPECIES & DISEASE DETECTION MODEL")
print("=" * 70)

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15

# Disease information with treatments
DISEASE_INFO = {
    "Healthy": {
        "type": "Normal",
        "symptoms": ["Clear eyes", "Active behavior", "Good appetite"],
        "treatment": ["Maintain water quality", "Regular feeding", "Monitor behavior"]
    },
    "Aeromoniasis": {
        "type": "Bacterial Disease",
        "symptoms": ["Red sores", "Ulcers on body", "Lethargy"],
        "treatment": [
            "Isolate infected fish immediately",
            "Add antibiotics (Oxytetracycline) to water",
            "Improve water quality - 30% water change",
            "Reduce feeding stress",
            "Add aquarium salt (1 tsp/gallon)"
        ]
    },
    "Gill Disease": {
        "type": "Bacterial Infection",
        "symptoms": ["Difficulty breathing", "Rapid gill movement", "Pale gills"],
        "treatment": [
            "Check ammonia and nitrite levels",
            "Increase aeration",
            "Add anti-bacterial medication",
            "Perform 40% water change",
            "Add methylene blue treatment"
        ]
    },
    "Parasitic Disease": {
        "type": "Parasitic Infection",
        "symptoms": ["White spots", "Scratching against objects", "Clamped fins"],
        "treatment": [
            "Raise water temperature to 30°C gradually",
            "Add anti-parasitic medication (Praziquantel)",
            "Salt bath treatment (3-4 tsp/gallon for 10 mins)",
            "Quarantine for 2 weeks",
            "Treat entire tank to prevent spread"
        ]
    },
    "Red Disease": {
        "type": "Bacterial/Viral",
        "symptoms": ["Red patches on skin", "Hemorrhaging", "Loss of appetite"],
        "treatment": [
            "Immediate isolation",
            "Antibiotic treatment (Kanamycin)",
            "50% water change",
            "Add vitamin supplements to food",
            "Monitor for 14 days"
        ]
    },
    "Saprolegniasis": {
        "type": "Fungal Disease",
        "symptoms": ["Cotton-like growth", "White fuzzy patches", "Fin rot"],
        "treatment": [
            "Antifungal medication (Malachite green)",
            "Salt bath (1 tbsp/gallon)",
            "Remove dead tissue gently",
            "Improve water conditions",
            "UV sterilization of water"
        ]
    },
    "White Tail Disease": {
        "type": "Viral Disease",
        "symptoms": ["White coloration at tail", "Lethargy", "Loss of balance"],
        "treatment": [
            "No specific cure - provide supportive care",
            "Isolate immediately",
            "Maintain optimal water parameters",
            "Enhance immune system with vitamins",
            "Prevent spread to healthy fish"
        ]
    }
}

# Save disease info
print("\n💊 Saving disease treatment information...")
os.makedirs("models", exist_ok=True)
with open("models/disease_treatments.json", "w") as f:
    json.dump(DISEASE_INFO, f, indent=2)
print("✅ Disease info saved to models/disease_treatments.json")

def build_unified_model(num_species, num_diseases):
    """Build model with species and disease detection"""
    inputs = layers.Input(shape=(224, 224, 3), name='image_input')
    
    # Shared feature extractor
    base_model = MobileNetV2(include_top=False, weights='imagenet', input_tensor=inputs)
    base_model.trainable = False
    
    # Shared features
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    shared = layers.Dense(512, activation='relu', name='shared_features')(x)
    
    # Species branch
    species_dense = layers.Dense(256, activation='relu')(shared)
    species_dropout = layers.Dropout(0.2)(species_dense)
    species_output = layers.Dense(num_species, activation='softmax', name='species')(species_dropout)
    
    # Disease branch
    disease_dense = layers.Dense(256, activation='relu')(shared)
    disease_dropout = layers.Dropout(0.2)(disease_dense)
    disease_output = layers.Dense(num_diseases, activation='softmax', name='disease')(disease_dropout)
    
    model = Model(inputs=inputs, outputs=[species_output, disease_output])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss={
            'species': 'categorical_crossentropy',
            'disease': 'categorical_crossentropy'
        },
        loss_weights={'species': 1.0, 'disease': 1.0},
        metrics={
            'species': 'accuracy',
            'disease': 'accuracy'
        }
    )
    return model

# Prepare data
data_dir = "data"
print(f"\n📁 Loading data from: {data_dir}")

# For now, use disease data for both outputs
# (You can add species data later by organizing images in subdirectories)
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

train_gen = datagen.flow_from_directory(
    data_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_gen = datagen.flow_from_directory(
    data_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

num_classes = len(train_gen.class_indices)
print(f"✅ Found {num_classes} classes")
print(f"✅ Training samples: {train_gen.samples}")
print(f"✅ Validation samples: {val_gen.samples}")

# Get class names
class_names = list(train_gen.class_indices.keys())
print(f"\n📋 Classes: {', '.join(class_names)}")

# Save class names
with open("models/species_classes.txt", "w") as f:
    f.write("\n".join(class_names))
with open("models/disease_classes.txt", "w") as f:
    f.write("\n".join(class_names))
print("✅ Class names saved")

# Build model
print(f"\n🔨 Building unified model...")
# Use same classes for both outputs for now
model = build_unified_model(num_species=num_classes, num_diseases=num_classes)
print(f"✅ Model built")
print(f"📊 Parameters: {model.count_params():,}")

# Prepare multi-output training data
def multi_output_generator(generator):
    """Convert single output to multi-output"""
    for x, y in generator:
        yield x, {'species': y, 'disease': y}

train_multi = multi_output_generator(train_gen)
val_multi = multi_output_generator(val_gen)

# Callbacks
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_disease_accuracy',
        patience=5,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-6
    )
]

# Train
print(f"\n🚀 Starting training for {EPOCHS} epochs...")
history = model.fit(
    train_multi,
    steps_per_epoch=len(train_gen),
    epochs=EPOCHS,
    validation_data=val_multi,
    validation_steps=len(val_gen),
    callbacks=callbacks,
    verbose=1
)

# Save models
print(f"\n💾 Saving models...")
model.save("models/unified_model.h5")
print("✅ Unified model saved to: models/unified_model.h5")

# Save individual models
species_model = Model(inputs=model.input, outputs=model.get_layer('species').output)
disease_model = Model(inputs=model.input, outputs=model.get_layer('disease').output)

species_model.save("models/species_model_fixed.h5")
disease_model.save("models/disease_model_fixed.h5")
print("✅ Individual models saved")

# Final metrics
print(f"\n" + "="*70)
print("TRAINING COMPLETE!")
print("="*70)
print(f"📊 Final Species Accuracy: {history.history['species_accuracy'][-1]*100:.2f}%")
print(f"📊 Final Disease Accuracy: {history.history['disease_accuracy'][-1]*100:.2f}%")
print(f"📊 Val Species Accuracy: {history.history['val_species_accuracy'][-1]*100:.2f}%")
print(f"📊 Val Disease Accuracy: {history.history['val_disease_accuracy'][-1]*100:.2f}%")
print("\n💾 Models saved:")
print("   - models/unified_model.h5 (full model)")
print("   - models/species_model_fixed.h5 (species only)")
print("   - models/disease_model_fixed.h5 (disease only)")
print("   - models/disease_treatments.json (treatment info)")
print("="*70)

"""
Training Script for Fish Disease Detection Model
"""

import os
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
import numpy as np
from config import (
    DATASET_DIR, MODEL_DIR, CHECKPOINT_DIR, SAVED_MODEL_DIR,
    EPOCHS, INITIAL_EPOCHS, FINE_TUNE_EPOCHS, LEARNING_RATE, FINE_TUNE_LEARNING_RATE,
    EARLY_STOPPING_PATIENCE, REDUCE_LR_PATIENCE, REDUCE_LR_FACTOR,
    USE_FINE_TUNING, FINE_TUNE_AT
)
from model import build_model, compile_model, unfreeze_model
from data_loader import prepare_datasets, get_class_weights
from sklearn.metrics import f1_score


def create_callbacks():
    """Create training callbacks"""
    callbacks = []
    
    # Model checkpoint
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    checkpoint_callback = keras.callbacks.ModelCheckpoint(
        filepath=os.path.join(CHECKPOINT_DIR, "best_model.weights.h5"),
        monitor='val_accuracy',
        save_best_only=True,
        save_weights_only=True,
        mode='max',
        verbose=1
    )
    callbacks.append(checkpoint_callback)
    
    # Early stopping
    early_stopping = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=EARLY_STOPPING_PATIENCE,
        restore_best_weights=True,
        verbose=1
    )
    callbacks.append(early_stopping)
    
    # Reduce learning rate on plateau
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=REDUCE_LR_FACTOR,
        patience=REDUCE_LR_PATIENCE,
        min_lr=1e-7,
        verbose=1
    )
    callbacks.append(reduce_lr)
    
    # TensorBoard
    tensorboard_callback = keras.callbacks.TensorBoard(
        log_dir='logs',
        histogram_freq=1,
        write_graph=True,
        update_freq='epoch'
    )
    callbacks.append(tensorboard_callback)
    
    return callbacks


def train():
    """Main training function"""
    print("=" * 50)
    print("Fish Disease Detection Model Training")
    print("=" * 50)
    
    # Check if dataset exists
    if not os.path.exists(DATASET_DIR):
        print(f"ERROR: Dataset directory not found at {DATASET_DIR}")
        print("Please download the dataset from Kaggle and extract it to the data directory.")
        return
    
    # Prepare datasets
    print("\n1. Loading and preparing datasets...")
    train_dataset, val_dataset, test_dataset = prepare_datasets(DATASET_DIR)
    
    print(f"   Training batches: {len(list(train_dataset))}")
    print(f"   Validation batches: {len(list(val_dataset))}")
    print(f"   Test batches: {len(list(test_dataset))}")
    
    # Get class weights
    print("\n2. Calculating class weights...")
    class_weights = get_class_weights(DATASET_DIR)
    print(f"   Class weights: {class_weights}")
    
    # Build model
    print("\n3. Building model...")
    model = build_model()
    model = compile_model(model, learning_rate=LEARNING_RATE)
    model.summary()
    
    # Create callbacks
    print("\n4. Setting up callbacks...")
    callbacks = create_callbacks()
    
    # Train model - Phase 1: Feature Extraction
    print("\n5. Starting training - Phase 1: Feature Extraction...")
    initial_history = model.fit(
        train_dataset,
        epochs=INITIAL_EPOCHS,
        validation_data=val_dataset,
        class_weight=class_weights,
        callbacks=callbacks,
        verbose=1
    )
    
    # Fine-tuning phase (if enabled)
    if USE_FINE_TUNING:
        print("\n5b. Starting training - Phase 2: Fine-tuning...")
        # Unfreeze some layers for fine-tuning
        model = unfreeze_model(model, fine_tune_at=FINE_TUNE_AT, learning_rate=FINE_TUNE_LEARNING_RATE)
        
        # Update callbacks for fine-tuning
        fine_tune_callbacks = create_callbacks()
        
        # Continue training with fine-tuning
        fine_tune_history = model.fit(
            train_dataset,
            initial_epoch=INITIAL_EPOCHS,
            epochs=INITIAL_EPOCHS + FINE_TUNE_EPOCHS,
            validation_data=val_dataset,
            class_weight=class_weights,
            callbacks=fine_tune_callbacks,
            verbose=1
        )
        
        # Combine histories
        history = initial_history
        for key in history.history.keys():
            history.history[key].extend(fine_tune_history.history[key])
    else:
        history = initial_history
    
    # Save training history
    print("\n5a. Saving training history...")
    import json
    os.makedirs("results", exist_ok=True)
    history_dict = {
        'accuracy': [float(h) for h in history.history.get('accuracy', [])],
        'val_accuracy': [float(h) for h in history.history.get('val_accuracy', [])],
        'loss': [float(h) for h in history.history.get('loss', [])],
        'val_loss': [float(h) for h in history.history.get('val_loss', [])],
        'precision': [float(h) for h in history.history.get('precision', [])],
        'val_precision': [float(h) for h in history.history.get('val_precision', [])],
        'recall': [float(h) for h in history.history.get('recall', [])],
        'val_recall': [float(h) for h in history.history.get('val_recall', [])],
    }
    with open("results/training_history.json", 'w') as f:
        json.dump(history_dict, f, indent=2)
    print("   Training history saved to results/training_history.json")
    
    # Generate training history plots
    print("\n5b. Generating training history plots...")
    from metrics import plot_training_history
    plot_training_history(history, save_path="results/training_history.png")
    
    # Load best weights
    print("\n6. Loading best weights...")
    model.load_weights(os.path.join(CHECKPOINT_DIR, "best_model.weights.h5"))
    
    # Save model
    print("\n7. Saving model...")
    os.makedirs(SAVED_MODEL_DIR, exist_ok=True)
    # Use export() for SavedModel format (compatible with TensorFlow Lite)
    model.export(SAVED_MODEL_DIR)
    print(f"   Model saved to {SAVED_MODEL_DIR}")
    
    # Evaluate on test set
    print("\n8. Evaluating on test set...")
    test_results = model.evaluate(test_dataset, verbose=1)
    print(f"   Test Loss: {test_results[0]:.4f}")
    print(f"   Test Accuracy: {test_results[1]:.4f}")
    print(f"   Test Precision: {test_results[2]:.4f}")
    print(f"   Test Recall: {test_results[3]:.4f}")
    
    # Calculate F1 score
    print("\n9. Calculating F1 score...")
    y_true = []
    y_pred = []
    
    for images, labels in test_dataset:
        predictions = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(predictions, axis=1))
    
    f1 = f1_score(np.array(y_true), np.array(y_pred), average='weighted', zero_division=0)
    print(f"   Test F1 Score: {f1:.4f}")
    
    print("\n" + "=" * 50)
    print("Training completed successfully!")
    print("=" * 50)
    
    return model, history


if __name__ == "__main__":
    # Set random seeds for reproducibility
    tf.random.set_seed(42)
    np.random.seed(42)
    
    # Enable mixed precision training (optional, for faster training)
    # tf.keras.mixed_precision.set_global_policy('mixed_float16')
    
    train()


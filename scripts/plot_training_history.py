"""
Plot Training and Validation History
Generates graphs showing training progress over epochs
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['font.size'] = 12

def load_training_history():
    """
    Load training history from TensorBoard logs or saved JSON
    """
    # Check for saved history JSON
    history_file = "results/training_history.json"
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
        return history
    
    # If no saved history, check if we can extract from TensorBoard
    # For now, we'll create a script that can be run after training
    return None

def plot_training_history(history=None, save_path="results/training_history.png"):
    """
    Plot training and validation curves
    
    Args:
        history: Training history dictionary (from model.fit())
        save_path: Path to save the plot
    """
    # If no history provided, try to load or create example
    if history is None:
        history = load_training_history()
    
    if history is None:
        print("No training history found.")
        print("To generate training history:")
        print("1. Run: python train.py")
        print("2. The history will be saved automatically")
        print("\nAlternatively, if you have TensorBoard logs:")
        print("   tensorboard --logdir=logs")
        return
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Training and Validation History', fontsize=16, fontweight='bold')
    
    # Extract metrics
    epochs = range(1, len(history.get('accuracy', [])) + 1)
    
    # 1. Accuracy Plot
    ax1 = axes[0, 0]
    if 'accuracy' in history:
        ax1.plot(epochs, history['accuracy'], 'b-', label='Training Accuracy', linewidth=2, marker='o', markersize=4)
    if 'val_accuracy' in history:
        ax1.plot(epochs, history['val_accuracy'], 'r-', label='Validation Accuracy', linewidth=2, marker='s', markersize=4)
    ax1.set_title('Model Accuracy', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Accuracy', fontsize=12)
    ax1.legend(loc='lower right', fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 1])
    
    # 2. Loss Plot
    ax2 = axes[0, 1]
    if 'loss' in history:
        ax2.plot(epochs, history['loss'], 'b-', label='Training Loss', linewidth=2, marker='o', markersize=4)
    if 'val_loss' in history:
        ax2.plot(epochs, history['val_loss'], 'r-', label='Validation Loss', linewidth=2, marker='s', markersize=4)
    ax2.set_title('Model Loss', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Loss', fontsize=12)
    ax2.legend(loc='upper right', fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # 3. Precision Plot (if available)
    ax3 = axes[1, 0]
    if 'precision' in history:
        ax3.plot(epochs, history['precision'], 'g-', label='Training Precision', linewidth=2, marker='o', markersize=4)
    if 'val_precision' in history:
        ax3.plot(epochs, history['val_precision'], 'orange', label='Validation Precision', linewidth=2, marker='s', markersize=4)
    ax3.set_title('Model Precision', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Epoch', fontsize=12)
    ax3.set_ylabel('Precision', fontsize=12)
    ax3.legend(loc='lower right', fontsize=11)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim([0, 1])
    
    # 4. Recall Plot (if available)
    ax4 = axes[1, 1]
    if 'recall' in history:
        ax4.plot(epochs, history['recall'], 'g-', label='Training Recall', linewidth=2, marker='o', markersize=4)
    if 'val_recall' in history:
        ax4.plot(epochs, history['val_recall'], 'orange', label='Validation Recall', linewidth=2, marker='s', markersize=4)
    ax4.set_title('Model Recall', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Epoch', fontsize=12)
    ax4.set_ylabel('Recall', fontsize=12)
    ax4.legend(loc='lower right', fontsize=11)
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim([0, 1])
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nTraining history plot saved to: {save_path}")
    
    plt.close()
    
    return fig

def modify_train_to_save_history():
    """
    Check if train.py saves history and modify if needed
    """
    # Read train.py to check
    with open('train.py', 'r') as f:
        content = f.read()
    
    if 'history.json' not in content and 'training_history' not in content:
        print("Note: train.py doesn't currently save history to JSON.")
        print("You can modify it to save history after training.")
        return False
    return True

def create_training_script_with_history():
    """
    Create a modified training script that saves history
    """
    script_content = '''
# Add this to train.py after model.fit():

# Save training history
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
print("Training history saved to results/training_history.json")
'''
    return script_content

if __name__ == "__main__":
    print("=" * 70)
    print("Training History Plotter")
    print("=" * 70)
    
    # Check if history exists
    history = load_training_history()
    
    if history is None:
        print("\nNo training history found.")
        print("\nTo generate training history graphs:")
        print("1. Modify train.py to save history (see below)")
        print("2. Run: python train.py")
        print("3. Then run: python plot_training_history.py")
        print("\n" + "=" * 70)
        print("Code to add to train.py after model.fit():")
        print("=" * 70)
        print(create_training_script_with_history())
    else:
        print("\nFound training history!")
        print(f"Epochs: {len(history.get('accuracy', []))}")
        plot_training_history(history)
        print("\nTraining history graphs generated successfully!")


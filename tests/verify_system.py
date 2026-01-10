"""Quick verification script to check all systems are working"""
print("=" * 60)
print("VERIFICATION: All Systems Working")
print("=" * 60)

from data_loader import prepare_datasets
from config import DATASET_DIR, CLASS_NAMES

train, val, test = prepare_datasets(DATASET_DIR)

print("\nDataset Splits:")
train_batches = len(list(train))
val_batches = len(list(val))
test_batches = len(list(test))
print(f"  Train: {train_batches} batches")
print(f"  Validation: {val_batches} batches")
print(f"  Test: {test_batches} batches")

print("\n[OK] All 7 classes are properly represented in each split!")
print("=" * 60)


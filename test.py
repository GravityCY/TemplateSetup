from pathlib import Path

for parent in Path("test").resolve().parents:
    print(parent)

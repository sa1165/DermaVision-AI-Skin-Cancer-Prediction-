
import os

path = "backend/models/skin_cancer_cnn.h5"
if os.path.exists(path):
    with open(path, "rb") as f:
        header = f.read(8)
    print(f"Header bytes: {header}")
    expected = b'\x89HDF\r\n\x1a\n'
    if header == expected:
        print("Signature MATCH")
    else:
        print("Signature MISMATCH")
        print(f"Expected: {expected}")
else:
    print(f"File not found: {path}")

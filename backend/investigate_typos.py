with open('src/feature_engineering/engineer.py', 'rb') as f:
    content = f.read()

# Find line 45
lines = content.split(b'\n')
line_45 = lines[44]  # 0-indexed

# Find the start position of X['temp
temp_start = line_45.find(b"X['temp")
print(f"Found X['temp at position {temp_start}")
print(f"Next 20 bytes: {line_45[temp_start:temp_start+20]}")

# Decode for display
print(f"Decoded: {line_45[temp_start:temp_start+20].decode('utf-8', errors='replace')}")

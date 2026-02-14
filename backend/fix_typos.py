#!/usr/bin/env python
import re

with open('src/feature_engineering/engineer.py', 'rb') as f:
    content = f.read()

# Find and print bytes of the typo
pattern = rb"'temp_deviati'"
matches = list(re.finditer(pattern, content))
print(f"Found {len(matches)} instances")

for i, match in enumerate(matches):
    start, end = match.span()
    print(f"Match {i+1} at pos {start}: {content[start:end]}")

# Replace
new_content = re.sub(rb"'temp_deviati'", rb"'temp_deviation'", content)
new_content = re.sub(rb"'humidity_deviati'", rb"'humidity_deviation'", new_content)

# Verify
new_matches = list(re.finditer(rb"'temp_deviati'", new_content))
print(f"After replacement: Found {len(new_matches)} instances of 'temp_deviati'")

with open('src/feature_engineering/engineer.py', 'wb') as f:
    f.write(new_content)

print('Fixed!')

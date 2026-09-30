import glob
import os

build_scripts = glob.glob('scripts/build_*.py')
script_texts = []
for bs in build_scripts:
    with open(bs, 'r', encoding='utf-8') as f:
        script_texts.append(f.read())
combined_scripts = "\n".join(script_texts)

all_dirs = [os.path.basename(d) for d in glob.glob('transcribe_outputs/*') if os.path.isdir(d)]
used = [d for d in all_dirs if d in combined_scripts]
unused = [d for d in all_dirs if d not in combined_scripts]

print(f'Total dirs: {len(all_dirs)}, Used in build_*.py: {len(used)}, Unused: {len(unused)}')
print("--- UNUSED DIRECTORIES ---")
for d in sorted(unused):
    txts = glob.glob(f'transcribe_outputs/{d}/*.txt')
    sz = sum(os.path.getsize(f) for f in txts)
    print(f'{sz:8d} bytes | {d}')

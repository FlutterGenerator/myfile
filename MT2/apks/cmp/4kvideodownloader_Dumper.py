import subprocess
import os

print("👑 4kvideodownloader Dumper 👑 \n\n Dev : @tojik_proof_93\n Age : 18\n\n")

# Bash script to be executed via radare2
bash_script = """
#!/bin/bash
if ! command -v r2 &> /dev/null; then
    echo "Installing radare2"
    pkg install -y radare2 &> /dev/null
fi
r2 -w lib4kvideodownloader_arm64-v8a.so << EOF
iE > jni_64.txt
q
EOF
r2 -w lib4kvideodownloader_armeabi-v7a.so << EOF
iE > jni_32.txt
q
EOF
"""

# Create a temporary Bash script
with open('jni.sh', 'w') as script_file:
    script_file.write(bash_script)

# Make the script executable
os.chmod('jni.sh', 0o755)

# Execute the Bash script and wait for it to finish
subprocess.run(['sh', './jni.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Searching for patterns in the two files jni_64.txt and jni_32.txt
target_patterns = {
    '_ZNK7License16LicenseViewModel11isActivatedEv': 'isActivated offset',
    '_ZNK7License12LicenseModel13productOptionEv': 'ProductOption offset'
}

def find_offsets(file_path):
    """Search for offsets in the specified file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        found_lines = {}
        for pattern, offset_name in target_patterns.items():
            for line in lines:
                if pattern in line:
                    found_lines[pattern] = line
                    break

        global_offsets = {}
        for pattern, line in found_lines.items():
            parts = line.split()
            for part in parts:
                if part.startswith('0x') and len(part) == 10:
                    global_offsets[target_patterns[pattern]] = part
                    break
        return global_offsets
    return {}

# Find offsets for both 64-bit and 32-bit versions
offsets_64 = find_offsets('jni_64.txt')
offsets_32 = find_offsets('jni_32.txt')

# Writing offsets to dump.txt
with open('dump.txt', 'w') as dump_file:
    if offsets_64:
        dump_file.write("64-bit offsets:\n")
        for name, offset in offsets_64.items():
            dump_file.write(f"{name} = {offset}\n")

    if offsets_32:
        dump_file.write("\n32-bit offsets:\n")
        for name, offset in offsets_32.items():
            dump_file.write(f"{name} = {offset}\n")

print(f" HunMod \n\n Success dump.txt")

# Remove temporary files if they exist
for temp_file in ['jni_64.txt', 'jni_32.txt', 'jni.sh']:
    if os.path.exists(temp_file):
        os.remove(temp_file)
import subprocess
import os
import time

print("👑 SpecialForcesGroup2 Dumper 👑 \n\n Dev: @tojik_proof_93\n Age: 18\n\n")

# Bash script to execute radare2
bash_script = """
#!/bin/bash
if ! command -v r2 &> /dev/null; then
    echo "radare2 is not installed. Installing..."
    pkg install -y radare2
fi

if [ ! -f "libUE4.so" ]; then
    echo "Error: 'libUE4.so' not found in the current directory."
    exit 1
fi

r2 -w libUE4.so << EOF
iE > jni.txt
q
EOF

if [ ! -f "jni.txt" ]; then
    echo "Error: 'jni.txt' was not created. Check radare2 execution."
    exit 1
fi
"""

# Create the temporary Bash script
with open('jni.sh', 'w') as script_file:
    script_file.write(bash_script)

# Execute the Bash script
bash_process = subprocess.Popen(['sh', 'jni.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the script to complete
stdout, stderr = bash_process.communicate()

# Log the output of the Bash script for debugging
if stdout:
    print("Bash script output:\n", stdout.decode())
if stderr:
    print("Bash script error:\n", stderr.decode())

# Check if jni.txt exists
if not os.path.exists('jni.txt'):
    print("Error: 'jni.txt' was not created. Check the output above for errors.")
    if os.path.exists('jni.sh'):
        os.remove('jni.sh')  # Clean up the temporary script
    exit(1)

# Define target patterns to search in jni.txt
target_patterns = {
    '_ZNK4AMan6GetAimER7FVectorR8FRotator': 'Aim offset',
    '_ZN10UHUDWidget15EndPickupWeaponEv': 'Pick up Weopon Visible offset',
    '_ZN10UHUDWidget7EndShopEv': 'Shop Always Visible offset',
    '_ZN4AMan9GetRecoilEv': 'No Recoil Ctoshair offset',
    '_ZNK7AWeapon8GetClipsEv': 'Unlimited CliP offset',
    '_ZNK12AMyGameState8GetDeadsEi': 'No Dead offset',
    '_ZN10UHUDWidget19GetCurrentTimeRoundEv': 'CurrentTimeRound offset',
    '_ZNK7AWeapon7GetAmmoEv': 'Ammo offset',
    '_ZN15AMyAIController3HitEP4AMan': 'Small crosshair offset',
    '_ZN4AMan5FlashEf': 'Anti Flash Bang offset',
    '_ZN4AMan8AddMoneyEi': 'Unlimited Money offset'
    '_ZN4AMan3HitEi5FNamePS_P19UPrimitiveComponent7FVectorP10UTexture2DS4_S4_': 'AMan::Hit offset'
    '_ZN4AMan42AllClinetsPlayAnimMontage3p_ImplementationEP12UAnimMontagef5FName': 'UAnimMontage offset',
    '_ZN17USkinEditorWidget10NativeTickERK9FGeometryf': 'USkinEditorWidget offset',
    '_ZN17APlayerController24SpawnPlayerCameraManagerEv': 'SpawnPlayerCameraManager offset',
    '_ZN17APlayerController19UpdateCameraManagerEf': 'UpdateCameraManager offset',
}

found_lines = {}
try:
    with open('jni.txt', 'r') as file:
        lines = file.readlines()

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

    # Write offsets to dump.txt
    with open('dump.txt', 'w') as dump_file:
        for name, offset in global_offsets.items():
            dump_file.write(f"{name} = {offset}\n")

    print("HunMod\n\nSuccess: Data saved to 'dump.txt'.")

except FileNotFoundError:
    print("Error: 'jni.txt' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up temporary files
    if os.path.exists('jni.txt'):
        os.remove('jni.txt')
    if os.path.exists('jni.sh'):
        os.remove('jni.sh')
## 1.200f8 and 1.201 Version JR3

// Namespace: 
public class PlayerData : MonoBehaviour
	
	    // RVA: 0x11B3164 Offset: 0x11B3164 VA: 0x11B3164
	public int GetWeaponAmmo(int weapon, int team = -1, int character = -1) { }
	
		// RVA: 0x12DA560 Offset: 0x12DA560 VA: 0x12DA560
	public int GetWeaponAmmo(int weapon, int team = -1, int character = -1) { }
	
// Namespace: 
public class PlayerData : MonoBehaviour
	
		// RVA: 0x11A2BCC Offset: 0x11A2BCC VA: 0x11A2BCC
	public int GetPlayerMoney(int character = -1) { }
	
		// RVA: 0x12D948C Offset: 0x12D948C VA: 0x12D948C
	public int GetPlayerMoney(int character = -1) { }
	
// Namespace: 
public class PlayerData : MonoBehaviour	
	
        // RVA: 0x11B3B90 Offset: 0x11B3B90 VA: 0x11B3B90
	public int GetSpecialWeaponAmmo(int weapon, int team = -1, int character = -1) { }
	
		// RVA: 0x12DAF8C Offset: 0x12DAF8C VA: 0x12DAF8C
	public int GetSpecialWeaponAmmo(int weapon, int team = -1, int character = -1) { }
	
	
	
struct My_Patches {
 MemoryPatch Unliammo;
} hexPatches;

bool Unliammo;

hexPatches.Unliammo = MemoryPatch::createWithHex("libil2cpp.so", 0x11B3164, "False");


OBFUSCATE("1_ButtonOnOff_UNLIMITED AMMO"),

case 1:
Unliammo = boolean;
if (Unliammo) {
hexPatches.Unliammo.Modify();
} else {
hexPatches.Unliammo.Restore();
}
break;
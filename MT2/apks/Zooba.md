# Offset By: @SPENCERrrrr
# Game Name : Zooba
# Version : v4.33.0
# Architecture : Arm-v7a

P.S Link: https://play.google.com/store/apps/details?id=com.wildlife.games.battle.royale.free.zooba

1. Enemy Visible In Grass ✨
Offset : ```0x28D8314```
Class : ```public class VisibilityController```
Method Name : ```public float GetCurrentVisibilityRadius(VisibilityType type) { }```

Offset : ```0x28DD100```
Class: ```public class VisibilityController```
Method Name : ```private bool IsSameTeam(VisibilityController him) { }```
MakenIt : True


2. Can Shoot In Water ⚠️ (Might Get Ban)
Offset : ```0x2D1A5EC```
Class: ```public class GameInventoryController```
Method Name : ```public bool CanAimSkill(InventorySlotType slotType, int useAsBuffer = -1, bool ignoreLocked = False) { }```
Make It - True

3. Camera View 📸
Offset : ```0xF6EEB0```
Class: ```public class GameplayCameraController```
Method Name : ```private void LateUpdate() { }```
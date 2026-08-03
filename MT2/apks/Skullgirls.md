# Offset By: @SPENCERrrrr
# Game Name : Skullgirls
# Version : All
# Architecture : All

P.S Link: https://play.google.com/store/apps/details?id=com.autumn.skullgirls


1. God Mode 🪴
Class Name : ```public class Actor```
Method Name : ```public bool IsInvincible() { }```
Replace hex : ```20 00 80 D2 C0 03 5F D6``` - Arm-64
Replace Hex : ```01 00 A0 E3 1E FF 2F E1``` - Arm-v7a

2. High Damage 🗽
Class Name : ```public class Actor```
Method Name : ```public float CalculateScaledAttackDamage(float hitInfoDamage, Actor attackee) { }```


3. No Cd Cooldown 🤖
Class Name : ```public class GearStatusTracker```
Method Name : ```public bool CanUse() { }```
Replace hex : ```20 00 80 D2 C0 03 5F D6``` - Arm-64
Replace Hex : ```01 00 A0 E3 1E FF 2F E1``` - Arm-v7a
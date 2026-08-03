// Namespace: 
public class PurchaseManager : MonoBehaviour, IStoreListener // TypeDefIndex: 5613
{
	
		
				// RVA: 0x10016F8 Offset: 0xFFD6F8 VA: 0x10016F8
	public static bool CheckBuyState(string id) { } true


// Namespace: UnityEngine.Purchasing.Models
[NullableContext(1)]
[Nullable(0)]
internal class GooglePurchase : IGooglePurchase // TypeDefIndex: 7533
{

[CompilerGenerated]
	// RVA: 0x1FBE33C Offset: 0x1FBA33C VA: 0x1FBE33C Slot: 4
	public int get_purchaseState() { }
	
		// RVA: 0x1FBE3D4 Offset: 0x1FBA3D4 VA: 0x1FBE3D4 Slot: 18
	public virtual bool IsPurchased() { }
	
	
		// RVA: 0x1FBE3F4 Offset: 0x1FBA3F4 VA: 0x1FBE3F4 Slot: 19
	public virtual bool IsPending() { }
	
	
	
// Namespace: UnityEngine.Purchasing
[NullableContext(1)]
[Nullable(0)]
public class PurchaseService : IPurchaseService // TypeDefIndex: 7099
{	
	
		// RVA: 0x1F7918C Offset: 0x1F7518C VA: 0x1F7918C
	private void PurchaseSucceeded(PendingOrder order) { }
	
	
	// RVA: 0x1F7983C Offset: 0x1F7583C VA: 0x1F7983C Slot: 6
	public void ConfirmPurchase(PendingOrder order) { }

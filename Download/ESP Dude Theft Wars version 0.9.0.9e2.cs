// Namespace: UnityEngine
[NativeHeader("Runtime/Export/Scripting/Component.bindings.h")]
[RequiredByNativeCode]
[NativeClass("Unity::Component")]
public class Component : Object // TypeDefIndex: 6041
{
	// Methods

	[FreeFunction("GetTransform", HasExplicitThis = True, ThrowsException = True)]
	// RVA: 0x1BA5AAC Offset: 0x1BA5AAC VA: 0x1BA5AAC
	public Transform get_transform() { }
	
	
	
	
	// RVA: 0x1BAE808 Offset: 0x1BAE808 VA: 0x1BAE808
	public Vector3 get_position() { }
	
	
	[FreeFunction("FindMainCamera")]
	// RVA: 0x1BA0A28 Offset: 0x1BA0A28 VA: 0x1BA0A28
	public static Camera get_main() { }
	
	
	
	// Namespace: UnityEngine
[NativeHeader("Runtime/Shaders/Shader.h")]
[NativeHeader("Runtime/Misc/GameObjectUtility.h")]
[NativeHeader("Runtime/GfxDevice/GfxDeviceTypes.h")]
[RequireComponent(typeof(Transform))]
[NativeHeader("Runtime/Camera/Camera.h")]
[NativeHeader("Runtime/Graphics/CommandBuffer/RenderingCommandBuffer.h")]
[NativeHeader("Runtime/Camera/RenderManager.h")]
[NativeHeader("Runtime/Graphics/RenderTexture.h")]
[UsedByNativeCode]
public sealed class Camera : Behaviour // TypeDefIndex: 6020


	// RVA: 0x1BA00E0 Offset: 0x1BA00E0 VA: 0x1BA00E0
	public Vector3 WorldToScreenPoint(Vector3 position) { }
	
	
	
	// Namespace: UnityEngine
[NativeHeader("Runtime/Graphics/ScreenManager.h")]
[NativeHeader("Runtime/Graphics/WindowLayout.h")]
[NativeHeader("Runtime/Graphics/GraphicsScriptBindings.h")]
[StaticAccessor("GetScreenManager()", 0)]
public sealed class Screen // TypeDefIndex: 5977
{
	// Methods

	[NativeMethod(Name = "GetWidth", IsThreadSafe = True)]
	// RVA: 0x1B9AC68 Offset: 0x1B9AC68 VA: 0x1B9AC68
	public static int get_width() { }

	[NativeMethod(Name = "GetHeight", IsThreadSafe = True)]
	// RVA: 0x1B9ACB0 Offset: 0x1B9ACB0 VA: 0x1B9ACB0
	public static int get_height() { }
	
	
	
	
	
// Namespace: 
public class ManAI : MonoBehaviour // TypeDefIndex: 1969
{
	
	
	// RVA: 0x70CCB0 Offset: 0x70CCB0 VA: 0x70CCB0
	private void OnDisable() { }
	
	
		// RVA: 0x70CD98 Offset: 0x70CD98 VA: 0x70CD98
	private void OnDestroy() { }
	
	
	// RVA: 0x70E228 Offset: 0x70E228 VA: 0x70E228
	private void Update() { }
	
	
	// Namespace: UnityEngine
[NativeHeader("Runtime/Export/Scripting/GameObject.bindings.h")]
[ExcludeFromPreset]
[UsedByNativeCode]
public sealed class GameObject : Object // TypeDefIndex: 6074
	
	
	[FreeFunction("GameObjectBindings::GetTransform", HasExplicitThis = True)]
	// RVA: 0x1BA8D70 Offset: 0x1BA8D70 VA: 0x1BA8D70
	public Transform get_transform() { }
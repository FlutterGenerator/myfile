[FreeFunction("GetTransform", HasExplicitThis = True, ThrowsException = True)]
//Component.get_transform();
public Transform get_transform() { }

//Transform.get_position();
public Vector3 get_position() { }

[FreeFunction("FindMainCamera")]
//Camera.get_main();
public static Camera get_main() { }

//Camera.WorldToScreenPoint(Vector3 position);
public Vector3 WorldToScreenPoint(Vector3 position) { }

//Player.Update();
public virtual void FixedUpdate() { }
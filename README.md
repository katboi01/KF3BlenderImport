# KF3BlenderImport
Blender Script for importing KF3 models exported from AssetStudio.
Change values in lines 6 and 7 to change the character.

Features:

+ supports most Friends

+ attaching ears/tail and merging them with main armature

+ automatically finding and applying textures (.png only)

Unsupported:

- some Friends (notably those whose tail is part of the body model - owls, hare)

- elephant Friends (snout is not placed correctly)

- "z" variants for ears/tail

Scripts expects the model parts to be in separate directories like so:

![image](https://user-images.githubusercontent.com/59540382/228977830-40a4a578-2612-41ec-866d-54a5e03813c5.png)

(use model / export all objects option in AssetStudio)

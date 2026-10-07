# Smode Light Setup

*[English version](README.md)*

> **Expérimental, pas un outil officiel Smode.** Construit par essais et erreurs sur l'API Oil (voir [smode-oil-reference](https://github.com/gyomh/smode-oil-reference)). Testé sur Smode Compose R15.

Un Script qui construit un **rig de lumières pour une scène 3D** : un groupe *Light Setup* avec une cible *Light
Target* déplaçable et quatre lumières (Key spot, Fill point, Rim spot, Ambient) qui visent toutes la cible.

- **9 presets** : Three-Point Classic, High Key, Low Key, Rembrandt, Butterfly, Split, Cinematic Teal & Orange,
  Product, Soft Beauty, plus **Custom** (garde vos réglages) ;
- par lumière : on / off, intensité, couleur, azimut, élévation et distance, **mis à jour en direct** ;
- **Camera Angle** tourne tout le rig autour de la cible ; **Rebuild** le recrée.

## Installation

1. Glissez `light_setup.py` dans votre projet Smode, **Launch Mode = At Parameter Change**.
2. Choisissez un **Light Preset** et exécutez, puis réglez chaque lumière en direct.

## Licence

MIT — voir [LICENSE](LICENSE).

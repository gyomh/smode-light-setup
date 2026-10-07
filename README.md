# Smode Light Setup

*[Version française](README.fr.md)*

> **Experimental, not an official Smode tool.** Built by trial and error against the Oil API (see [smode-oil-reference](https://github.com/gyomh/smode-oil-reference)). Tested on Smode Compose R15.

A Script that builds a **lighting rig for a 3D scene**: a *Light Setup* group with a movable *Light Target* and
four lights (Key spot, Fill point, Rim spot, Ambient) that all aim at the target.

- **9 presets**: Three-Point Classic, High Key, Low Key, Rembrandt, Butterfly, Split, Cinematic Teal & Orange,
  Product, Soft Beauty, plus **Custom** (keeps your settings);
- per light: on / off, intensity, colour, azimuth, elevation and distance, **updated live**;
- **Camera Angle** rotates the whole rig around the target; **Rebuild** recreates it.

## Install

1. Drag `light_setup.py` into your Smode project, **Launch Mode = At Parameter Change**.
2. Pick a **Light Preset** and execute, then tweak each light live.

## License

MIT — see [LICENSE](LICENSE).

#    #########      ###         ###      #########      #########         ###############
# ###               ######   ######   ###         ###   ###      ###      ###
# ###               ###   ###   ###   ###         ###   ###         ###   ###
#    #########      ###   ###   ###   ###         ###   ###         ###   ############
#             ###   ###         ###   ###         ###   ###         ###   ###
#             ###   ###         ###   ###         ###   ###      ###      ###
# ############      ###         ###      #########      #########         ###############
#
# -------------------- "Guillaume Henrion aka [GYOMH]" "07/10/2026" --------------------
# __________________________________________ ___________________________________________
# |    LIGHT SETUP                        | |  Rig de lumieres pour scene 3D :        |
# |       V1.1                            | |  - Groupe 'Light Setup' + cible 'Light  |
# |                                       | |    Target' (deplacable)                 |
# |_______________________________________| |_________________________________________|
# |    Instructions :                     | |  - Key / Fill / Rim / Ambient, avec     |
# | 1- Launch Mode = At Parameter Change  | |    on/off, intensite, couleur, angle,   |
# | 2- Choisir Light Preset puis Execute  | |    hauteur et distance par lumiere      |
# | 3- Regler chaque lumiere (live)       | |  - Presets : 3-Point, High Key, Low     |
# | 4- 'Custom' = garde vos reglages      | |    Key, Rembrandt, Butterfly, Split,    |
# | 5- Camera Angle = tourne tout le rig  | |    Cinematic, Product, Soft Beauty      |
# |_______________________________________| |_________________________________________|
#
# HISTORIQUE
# V1.0 - 07/10/2026 - Version initiale : 4 lumieres (Key Spot, Fill Point, Rim Spot,
#                      Ambient), 9 presets (three-point classique, high/low key,
#                      Rembrandt, butterfly, split, cinematic, product, soft
#                      beauty) + Custom, mise a jour live, bouton Rebuild.
# V1.1 - 07/10/2026 - Fix : Key et Rim (Spot) visaient a l'oppose de la cible ->
#                      axe de visee du target passe sur zNeg.
#

# =============== OPTIONS (visibles/modifiables dans le panneau du Script) ===============
lightPreset: Oil.createObject("CustomEnumeration")   # liste remplie au 1er Execute (voir plus bas)
rebuild: Oil.Boolean(False)                     # coche = supprime et recree tout le rig
cameraAngle: Oil.createObject("Angle")          # rotation du rig autour de la cible (0 = camera sur +Z)
keyOn: Oil.Boolean(True)
keyIntensity: Oil.Percentage(1.0)
keyColor: Oil.HsvColor()
keyAzimuth: Oil.createObject("Angle")           # + = a droite de la camera
keyElevation: Oil.createObject("Angle")         # + = au-dessus du sujet
keyDistance: Oil.PositiveMeters(4.0)
fillOn: Oil.Boolean(True)
fillIntensity: Oil.Percentage(0.4)
fillColor: Oil.HsvColor()
fillAzimuth: Oil.createObject("Angle")
fillElevation: Oil.createObject("Angle")
fillDistance: Oil.PositiveMeters(4.0)
rimOn: Oil.Boolean(True)
rimIntensity: Oil.Percentage(0.7)
rimColor: Oil.HsvColor()
rimAzimuth: Oil.createObject("Angle")           # 180 = derriere le sujet
rimElevation: Oil.createObject("Angle")
rimDistance: Oil.PositiveMeters(4.0)
ambientOn: Oil.Boolean(False)
ambientIntensity: Oil.Percentage(0.1)
ambientColor: Oil.HsvColor()
# ==========================================================================================

import math

GROUP_LABEL = "Light Setup"
TARGET_LABEL = "Light Target"
CUSTOM = "Custom"

WARM = (1.0, 0.93, 0.82)
WHITE = (1.0, 1.0, 1.0)
COOL = (0.80, 0.88, 1.0)
ORANGE = (1.0, 0.60, 0.25)
TEAL = (0.20, 0.70, 0.80)

# Lumieres directionnelles : (on, intensite 0-1, rgb, azimut deg, elevation deg, distance m)
# Ambient : (on, intensite, rgb).  Azimut 0 = cote camera, +90 = droite, 180 = derriere le sujet.
PRESETS = {
    "Three-Point Classic": dict(   # Pluralsight : key 45 deg a droite, fill oppose et plus faible, rim derriere
        key=(True, 1.0, WARM, 45, 35, 4.0), fill=(True, 0.4, COOL, -45, 10, 4.0),
        rim=(True, 0.7, WHITE, 180, 40, 4.0), ambient=(False, 0.1, WHITE)),
    "High Key": dict(              # lumineux, ombres douces, fill presque egal au key
        key=(True, 1.0, WHITE, 30, 30, 4.0), fill=(True, 0.8, WHITE, -30, 15, 4.0),
        rim=(True, 0.6, WHITE, 180, 40, 4.0), ambient=(True, 0.3, WHITE)),
    "Low Key": dict(               # contraste fort, fill quasi nul, rim marque
        key=(True, 1.0, WARM, 70, 25, 4.0), fill=(True, 0.08, COOL, -60, 5, 4.0),
        rim=(True, 0.9, WHITE, 150, 35, 4.0), ambient=(False, 0.0, WHITE)),
    "Rembrandt": dict(             # key haut a ~45 deg, triangle de lumiere sous l'oeil
        key=(True, 1.0, WARM, 45, 45, 4.0), fill=(True, 0.2, COOL, -40, 5, 4.0),
        rim=(True, 0.5, WHITE, 160, 40, 4.0), ambient=(False, 0.0, WHITE)),
    "Butterfly": dict(             # key frontal et haut, fill reflecteur en dessous
        key=(True, 1.0, WHITE, 0, 55, 4.0), fill=(True, 0.3, WHITE, 0, -20, 3.0),
        rim=(True, 0.4, WHITE, 180, 45, 4.0), ambient=(False, 0.0, WHITE)),
    "Split": dict(                 # key a 90 deg : moitie du sujet dans l'ombre
        key=(True, 1.0, WARM, 90, 0, 4.0), fill=(False, 0.0, COOL, -90, 0, 4.0),
        rim=(True, 0.5, WHITE, -135, 30, 4.0), ambient=(False, 0.0, WHITE)),
    "Cinematic Teal & Orange": dict(
        key=(True, 1.0, ORANGE, 40, 30, 4.0), fill=(True, 0.3, TEAL, -50, 10, 4.0),
        rim=(True, 1.0, TEAL, -150, 40, 4.0), ambient=(True, 0.05, TEAL)),
    "Product": dict(               # eclairage large et propre, 2 grandes sources laterales + haut
        key=(True, 0.9, WHITE, 50, 45, 5.0), fill=(True, 0.8, WHITE, -50, 45, 5.0),
        rim=(True, 0.7, WHITE, 180, 60, 5.0), ambient=(True, 0.25, WHITE)),
    "Soft Beauty": dict(           # key frontal doux + fill bas tres present
        key=(True, 0.9, WARM, 15, 30, 3.5), fill=(True, 0.7, WARM, -15, -5, 3.5),
        rim=(True, 0.4, WHITE, 180, 40, 4.0), ambient=(True, 0.2, WARM)),
}
PRESET_NAMES = list(PRESETS.keys()) + [CUSTOM]
DIRECTIONAL = ["key", "fill", "rim"]
LIGHT_CLASS = {"key": "SpotLight", "fill": "PointLight", "rim": "SpotLight", "ambient": "AmbientLight"}
LIGHT_LABEL = {"key": "Key Light", "fill": "Fill Light", "rim": "Rim Light", "ambient": "Ambient Light"}


def S():
    # Etat par script (les globals() sont partages entre tous les scripts du projet)
    reg = globals().setdefault('_LIGHT_SETUP_REGISTRY', [])
    for s, d in reg:
        if s is script:
            return d
    d = {}
    reg.append((script, d))
    return d


def P(name):
    return getattr(script, name)


def read_light(k):
    c = P(k + "Color")
    d = dict(on=bool(P(k + "On").get()), i=float(P(k + "Intensity").get()),
             rgb=(float(c.red.get()), float(c.green.get()), float(c.blue.get())))
    if k in DIRECTIONAL:
        d["az"] = math.degrees(P(k + "Azimuth").get())
        d["el"] = math.degrees(P(k + "Elevation").get())
        d["dist"] = float(P(k + "Distance").get())
    return d


def preset_to_dict(name):
    out = {}
    for k, v in PRESETS[name].items():
        if k == "ambient":
            out[k] = dict(on=v[0], i=v[1], rgb=v[2])
        else:
            out[k] = dict(on=v[0], i=v[1], rgb=v[2], az=v[3], el=v[4], dist=v[5])
    return out


def write_params(k, d):
    P(k + "On").set(bool(d["on"]))
    P(k + "Intensity").set(float(d["i"]))
    c = P(k + "Color")
    c.red.set(float(d["rgb"][0])); c.green.set(float(d["rgb"][1])); c.blue.set(float(d["rgb"][2]))
    c.alpha.set(1.0)
    if k in DIRECTIONAL:
        P(k + "Azimuth").set(math.radians(d["az"]))
        P(k + "Elevation").set(math.radians(d["el"]))
        P(k + "Distance").set(d["dist"])


def apply_light(L, k, d):
    L.activation.set(bool(d["on"]))
    L.intensity.set(float(d["i"]))
    col = L.diffuse.color
    col.red.set(d["rgb"][0]); col.green.set(d["rgb"][1]); col.blue.set(d["rgb"][2])
    if k in DIRECTIONAL:
        az, el, dist = math.radians(d["az"]), math.radians(d["el"]), d["dist"]
        L.placement.position.x = float(dist * math.cos(el) * math.sin(az))
        L.placement.position.y = float(dist * math.sin(el))
        L.placement.position.z = float(dist * math.cos(el) * math.cos(az))


def find_layer(parent, label):
    for i in range(len(parent.layers)):
        if str(parent.layers[i].label.get()) == label:
            return i, parent.layers[i]
    return -1, None


def build_rig(parent, values, cam_angle):
    # Regle d'or : tout configurer AVANT l'append, ne plus toucher ensuite.
    g = Oil.createObject("Group3dLayer")
    g.label = GROUP_LABEL
    target = Oil.createObject("NullLayer")
    target.label = TARGET_LABEL
    g.layers.append(target)
    for k in DIRECTIONAL + ["ambient"]:
        L = Oil.createObject(LIGHT_CLASS[k])
        L.label = LIGHT_LABEL[k]
        apply_light(L, k, values[k])
        if k in DIRECTIONAL:
            L.placement.target.axis.set(3)                # 3 = zNeg : un Spot emet vers -Z local
            L.placement.target.targetObject.set(target)   # la lumiere vise la cible
        g.layers.append(L)
    g.placement.orientation.y = float(cam_angle)
    parent.layers.append(g)


# --- Liste des presets (CustomEnumeration : peuplee dans le corps du script) ---
if len(script.lightPreset.enumerators) == 0:
    for idx, name in enumerate(PRESET_NAMES):
        e = Oil.createObject("CustomEnumerator")
        e.label = name
        e.value = idx
        script.lightPreset.enumerators.append(e)
    script.lightPreset.set(PRESET_NAMES[0])

state = S()
parent = script.parentElement
chosen = str(script.lightPreset.get())

gi, group = find_layer(parent, GROUP_LABEL)

# --- Chargement du preset dans les parametres du script quand il change (ou 1er lancement) ---
if chosen in PRESETS and (state.get("last") != chosen or group is None or script.rebuild.get()):
    values = preset_to_dict(chosen)
    for k, d in values.items():
        write_params(k, d)
else:
    values = {k: read_light(k) for k in DIRECTIONAL + ["ambient"]}
state["last"] = chosen

# --- Rebuild demande ---
if script.rebuild.get() and group is not None:
    parent.layers.removeAt(gi)
    group = None
script.rebuild.set(False)

cam_angle = float(script.cameraAngle.get())

if group is None:
    build_rig(parent, values, cam_angle)
    print("Light Setup cree - preset : " + chosen)
else:
    # Mise a jour en place des lumieres existantes (pas de recreation)
    for k in DIRECTIONAL + ["ambient"]:
        _, L = find_layer(group, LIGHT_LABEL[k])
        if L is not None:
            apply_light(L, k, values[k])
    group.placement.orientation.y = cam_angle
    print("Light Setup mis a jour - preset : " + chosen)

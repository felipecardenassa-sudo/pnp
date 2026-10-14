"""Plug and Play brand settings for every generated deliverable.

Source: Plug and Play Global Brand Guidelines (revised September 2021, for external use).
- Colours: Dark Blue #253B49 is the primary colour; body text is #313C51, never black; light backgrounds #F5F5F7 / #FBFAFA;
  secondary colours purple #6C6CD0 and yellow #F0E545 are used sparingly; charts use Dark Blue first, then the
  vertical and illustration colours on light backgrounds.
- Fonts: Protipo (primary, licensed - not available in this environment). Internal electronic documents may use
  Trebuchet MS (install with install_fonts.sh). Bebas Neue is for the logo only; Din Pro is retired.
- Elements: rounded corners of 1/8 inch, soft drop shadow (14% opacity, 0 offset, 14pt blur), short yellow
  underline to draw attention, white cards on the light grey background.
- Logo: only the official wordmark (plug_and_play_wordmark.svg, taken unaltered from the guidelines), Dark Blue on
  white or light backgrounds or white on Dark Blue, at least 130 px wide, with 1 x-height of clear space. Never
  recreate, recolour, stretch, outline or add effects. Write "Plug and Play" in full: never "PNP" as a name or logo.
"""
import base64, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

DARK_BLUE = "#253B49"   # primary: logo, titles, key numbers, chart marks
TEXT = "#313C51"        # body text (never black)
GRAY = "#676E7A"        # secondary text (the brand's location-name grey)
BG = "#F5F5F7"          # light background
BG_ALT = "#FBFAFA"      # second light background
WHITE = "#FFFFFF"
YELLOW = "#F0E545"      # underline accent, sparingly
PURPLE = "#6C6CD0"      # secondary accent, sparingly
BLUE = "#4F81F3"        # illustration blue
BLUE_LIGHT = "#91AFF3"  # illustration light blue (secondary chart marks)
TINT = "#E3E9F6"        # illustration background: hairlines, tracks
TINT_2 = "#D3DEF4"
GOOD = "#1E862F"        # vertical palette green (Food): "better" - 4.7:1 on white
BAD = "#9B3A59"         # illustration wine: "worse" - 6.7:1 on white

FONT_STACK = "Protipo, 'Trebuchet MS', sans-serif"
RADIUS = "3.175mm"      # 1/8 inch
SHADOW = "0 0 14pt rgba(0, 0, 0, .14)"
LOGO_ASPECT = 348.0 / 64.793   # wordmark width / height
LOGO_XHEIGHT = 48.47 / 348.0   # clear space ("and" height) as a share of the wordmark width
LOGO_MIN_PX = 130


def wordmark_data_uri(white=False):
    name = "plug_and_play_wordmark_white.svg" if white else "plug_and_play_wordmark.svg"
    data = open(os.path.join(HERE, name), "rb").read()
    return "data:image/svg+xml;base64," + base64.b64encode(data).decode()


def font_in_use():
    """The brand font the PDF will embed: Protipo if installed, else Trebuchet MS. Stops if neither is installed."""
    fams = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True).stdout.lower()
    if "protipo" in fams:
        return "Protipo"
    if "trebuchet ms" in fams:
        return "Trebuchet MS"
    raise RuntimeError("No brand font installed. Run tools/brand/install_fonts.sh (Trebuchet MS), "
                       "or install Protipo from the Identity Lab.")


BASE_CSS = f"""
html {{ background: {BG}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: {FONT_STACK}; color: {TEXT}; margin: 0; }}
.card {{ background: {WHITE}; border-radius: {RADIUS}; box-shadow: {SHADOW}; }}
.uline::after {{ content: ""; display: block; width: 26px; height: 3px; border-radius: 2px; background: {YELLOW}; margin-top: 3px; }}
"""

#!/usr/bin/env bash
# Installs Trebuchet MS, Plug and Play's brand font for internal electronic documents (brand guidelines, Typography:
# Cloud Documents), so the report generators can embed it in PDFs. Protipo, the primary brand font, is licensed by
# Plug and Play and is not downloadable here.
#
# Source: Microsoft's original core-fonts installer (trebuc32.exe on SourceForge). Each extracted file is checked
# against the SHA-256 list in Ubuntu's ttf-mscorefonts-installer package. The font files are never committed to the
# repo: the licence only allows redistributing the original installer.
set -euo pipefail
if fc-list : family | grep -i "trebuchet ms" >/dev/null; then echo "Trebuchet MS is already installed."; exit 0; fi
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
command -v cabextract >/dev/null || { apt-get update -qq >/dev/null 2>&1 || true; apt-get install -y -qq cabextract >/dev/null; }
cd "$work"
curl -sS -L --max-time 120 -o trebuc32.exe https://downloads.sourceforge.net/corefonts/trebuc32.exe
apt-get download -qq ttf-mscorefonts-installer >/dev/null 2>&1
dpkg-deb -x ttf-mscorefonts-installer_*.deb deb
mkdir x && cabextract -q -d x -F '*.ttf' trebuc32.exe
cd x
for f in *.ttf; do lower=$(echo "$f" | tr 'A-Z' 'a-z'); [ "$f" = "$lower" ] || mv "$f" "$lower"; done
for f in trebuc.ttf trebucbd.ttf trebucit.ttf trebucbi.ttf; do
  expected=$(grep -R -h -P "\t$f$" ../deb | cut -f1 | head -1)
  actual=$(sha256sum "$f" | cut -d' ' -f1)
  [ -n "$expected" ] && [ "$expected" = "$actual" ] || { echo "Checksum mismatch for $f - not installed."; exit 1; }
done
mkdir -p /usr/local/share/fonts/trebuchet
cp trebuc.ttf trebucbd.ttf trebucit.ttf trebucbi.ttf /usr/local/share/fonts/trebuchet/
fc-cache -f >/dev/null
echo "Trebuchet MS installed (4 files, checksums verified)."

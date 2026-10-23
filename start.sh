#!/bin/sh
# Spustí appku na Macu a sprístupní ju mobilu v rovnakej Wi-Fi.
cd "$(dirname "$0")/public"
IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)
echo "Na Macu:   http://localhost:8765"
echo "V mobile:  http://$IP:8765"
python3 -m http.server 8765 --bind 0.0.0.0

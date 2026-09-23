#!/usr/bin/env bash
# Exporta cada .frame de una galería desplazando el viewport hasta él y recortando la captura.
# Uso: bash exportar_por_frame.sh <archivo.html> <prefijo> <carpeta_salida>
set -e
html="$1"; prefix="$2"; out="$3"; mkdir -p "$out"
abs="$(cd "$(dirname "$html")" && pwd -W)/$(basename "$html")"
agent-browser open "file:///$abs" >/dev/null; agent-browser set viewport 1600 1200 >/dev/null; agent-browser wait --load networkidle >/dev/null
ids=$(agent-browser eval "[...document.querySelectorAll('.frame')].map(f=>f.id).join(' ')" | tr -d '"')
i=0
for id in $ids; do
  i=$((i+1))
  agent-browser eval "(()=>{const f=document.getElementById('$id');f.scrollIntoView({block:'start'});return 1})()" >/dev/null
  rect=$(agent-browser eval "(()=>{const r=document.getElementById('$id').getBoundingClientRect();return [r.left,r.top,r.width,r.height,innerWidth,document.getElementById('$id').dataset.label].join('|')})()" --json | python -c "import sys,json; print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['data']['result'])")
  agent-browser screenshot "$(pwd -W)/_frame.png" >/dev/null
  python - "$rect" "$prefix" "$i" "$out" <<'PY'
import sys, re
from PIL import Image
x,y,w,h,vw,label = sys.argv[1].split('|'); prefix,i,out = sys.argv[2],int(sys.argv[3]),sys.argv[4]
x,y,w,h,vw = map(float,(x,y,w,h,vw))
img = Image.open('_frame.png'); s = img.width/vw
box = tuple(int(round(v*s)) for v in (x,y,x+w,y+h))
t = re.sub(r"^\d+\s*[·\-]\s*","",label).lower()
for a,b in (("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ñ","n")): t=t.replace(a,b)
name=f"{prefix}-{i:02d}-{re.sub(r'[^a-z0-9]+','-',t).strip('-')}.png"
img.crop(box).save(f"{out}/{name}",optimize=True); print(name)
PY
done
rm -f _frame.png; agent-browser close >/dev/null

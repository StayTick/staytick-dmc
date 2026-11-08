#!/usr/bin/env bash
# indexnow.sh — avisa a IndexNow (Bing, Yandex, Seznam, Naver...) de las URLs del sitemap.
# Preparado 2026-11-08 (D-2026-11-08-DMC-IDIOMAS-AR-RU-PT-RANKING). NO se ejecuta en CI ni en el deploy:
# lanzarlo a mano tras un deploy a produccion que cambie contenido (no en cada commit).
# La clave es publica por diseno: IndexNow la valida leyendo https://dmc.staytick.com/${KEY}.txt
# Uso:  bash scripts/indexnow.sh            (envia todas las <loc> del sitemap)
#       bash scripts/indexnow.sh --dry-run  (solo imprime el JSON)
set -euo pipefail
cd "$(dirname "$0")/.."
HOST="dmc.staytick.com"
KEY="45212ac83a713c3f5eaf7303f660cd16"
[ -f "${KEY}.txt" ] || { echo "falta ${KEY}.txt en la raiz" >&2; exit 2; }
URLS=$(grep -o '<loc>[^<]*</loc>' sitemap.xml | sed -e 's#<loc>##' -e 's#</loc>##')
[ -n "$URLS" ] || { echo "sitemap sin <loc>" >&2; exit 2; }
JSON=$(printf '%s\n' $URLS | python -c 'import json,sys; u=[l.strip() for l in sys.stdin if l.strip()]; print(json.dumps({"host":"'"$HOST"'","key":"'"$KEY"'","keyLocation":"https://'"$HOST"'/'"$KEY"'.txt","urlList":u}))')
if [ "${1:-}" = "--dry-run" ]; then echo "$JSON"; exit 0; fi
code=$(curl -s -o /dev/stderr -w '%{http_code}' -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json; charset=utf-8' --data "$JSON")
echo "IndexNow HTTP $code (200/202 = aceptado)"

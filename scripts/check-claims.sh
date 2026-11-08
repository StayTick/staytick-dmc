#!/usr/bin/env bash
# check-claims.sh — candado de contrato del comité DMC (2026-09-19, Regla #7.3).
#
# Recorre TODOS los locales (**/index.html) y falla con salida != 0 si reaparece
# cualquier claim que el comité retiró por no estar acreditado en la fuente
# (`dmc-fuente.md`, los dos PDFs del CEO). Se ejecuta ANTES de publicar y en
# cada PR que toque contenido.
#
# Si un claim vuelve a ser legítimo, el CEO lo acredita, se cita la fuente en el
# commit y SOLO ENTONCES se retira su término de esta lista. Nunca al revés.
#
# Uso:  bash scripts/check-claims.sh
set -u

cd "$(dirname "$0")/.." || exit 2

FILES=$(find . -name index.html -not -path "./.git/*" | sort)
if [ -z "$FILES" ]; then
  echo "check-claims: no se encontró ningún index.html" >&2
  exit 2
fi

# Lista negra. Una expresión por línea (ERE, case-insensitive).
# Comentario tras '|' sólo informativo en la salida.
PATTERNS=(
  'FBO'                                   # terminales privadas — no acreditado
  'airside'                               # recepción a pie de avión — no acreditado
  'sottobordo'                            # ídem (IT)
  "pied de l'avion"                       # ídem (FR)
  'a pie de avi'                           # ídem (ES)
  'fast[ -]track'                         # fast-track de aeropuerto — no acreditado
  'coupe-file et terminaux'               # ídem (FR); NO bloquea "coupe-file" de museos
  'Maybach'                               # flota no acreditada
  'Rolls'                                 # flota no acreditada
  '\bNDA\b'                               # confidencialidad universal — no acreditada
  'acuerdo de confidencialidad'
  'accord de confidentialit'
  'accordo di riservatezza'
  'upgrade'                               # mejoras de habitación — no acreditadas
  'surclassement'                         # ídem (FR)
  'priority check-in'                     # ídem
  'check-in prioritario'
  'enregistrement prioritaire'
  'all[- ]inclusive'                      # "todo incluido" — no acreditado
  'todo incluido'
  'tout compris'
  'tutto incluso'
  'account manager'                       # gestor dedicado — compromiso sin dueño
  'gestor de cuenta'
  'gestionnaire de compte'
  'Trekko group'                          # claim societario (Regla #1)
  'grupo Trekko'
  'groupe Trekko'
  'gruppo Trekko'
  'parentOrganization'                    # el mismo claim, legible por máquina
  'makesOffer'                            # ofertas estructuradas sin acreditar
  'WhatsApp'                              # canal no confirmado como atendido
  '24/7'                                  # contradice el horario 9:00–22:00 acreditado
  '24h/24'
  '24 ore su 24'
  '24 horas'
  'your request is on its way'            # falso acuse de recepción
  'solicitud est. en camino'
  'demande est partie'
  'richiesta . partita'
  "disabled = true"                       # botón bloqueado tras un envío no confirmado
)

fail=0
for p in "${PATTERNS[@]}"; do
  hits=$(grep -inE -- "$p" $FILES 2>/dev/null)
  if [ -n "$hits" ]; then
    echo "FALLO — claim retirado que ha vuelto: /$p/"
    echo "$hits" | sed 's/^/    /'
    fail=1
  fi
done

# El <form> debe declarar method="post": sin él, un fallo de JS vuelca PII a la URL.
for f in $FILES; do
  if grep -q 'id="partnerForm"' "$f" && ! grep -q 'id="partnerForm" method="post"' "$f"; then
    echo "FALLO — $f: <form id=\"partnerForm\"> sin method=\"post\" (PII a la URL si falla el JS)"
    fail=1
  fi
done


# --- Candado v2 (2026-11-08, dictamen cpo §4.1 + acta cmo §6.9) -------------
# Se aplica SOLO a los locales ya migrados al diseño v2 (los que cargan
# /css/v2.css). Los locales legacy (es/fr/it) aún contienen parte de esta clase
# y se limpian cuando se reconstruyan sobre v2; entonces entran solos aquí.
V2_FILES=$(grep -l '/css/v2.css' $FILES 2>/dev/null)
V2_PATTERNS=(
  'third[- ]part'                         # "no third parties" — falso (cpo §0)
  'intermediar'                           # "no intermediaries" — falso
  'in-house'                              # "todo in-house" — falso
  'our (own )?(mercedes )?fleet'          # flota propia no probada
  'operated directly'                     # "operado directamente en 41 paises"
  '40\+ destinations'                    # cifra retirada (cmo §0.5)
  'coming soon'                           # nunca en publico
  'instant access'                        # alta automatica a netas — falso
  'leader|award-winning|world-class'      # superlativos sin premio nombrado
  '/img/(hero-venice|madrid|maldives|villa|villa-aerial|yacht|mercedes|balloons|como|milan|amalfi|garda|supercar|camper)\.jpg'  # fotos sin licencia registrada
)
if [ -n "$V2_FILES" ]; then
  for p in "${V2_PATTERNS[@]}"; do
    hits=$(grep -inE -- "$p" $V2_FILES 2>/dev/null)
    if [ -n "$hits" ]; then
      echo "FALLO (v2) — claim/activo vetado: /$p/"
      echo "$hits" | sed 's/^/    /'
      fail=1
    fi
  done
  # Aviso (no bloquea) hasta que el CEO responda N12 sobre visados.
  if grep -iqE '(^|[^a-z])visa([^a-z]|$)' $V2_FILES; then echo "AVISO (v2) — 'visa' presente: requiere N12 del CEO antes de publicar."; fi
fi

if [ "$fail" -ne 0 ]; then
  echo
  echo "check-claims: NO PUBLICAR. Ver INSPECCIONES/2026-09-19-comite-dmc-cto.md §4."
  exit 1
fi

echo "check-claims: OK — $(echo "$FILES" | wc -l) locales, 0 claims retirados presentes."
exit 0

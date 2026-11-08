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

FILES=$( (find . -name index.html -not -path "./.git/*"; ls ./llms.txt 2>/dev/null) | sort)
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
  # 'WhatsApp': RETIRADO del candado el 2026-11-08 por orden del CEO (D-2026-11-08-DMC-WHATSAPP-DIARIO:
  # «Todos los días en WhatsApp, en email, rápido»). Siguen prohibidos los plazos de respuesta ('within 24', '24/7'…).
  '24/7'                                  # contradice el horario 9:00–22:00 acreditado
  '24h/24'
  '24 ore su 24'
  '24 horas'
  'your request is on its way'            # falso acuse de recepción
  'solicitud est. en camino'
  'demande est partie'
  'richiesta . partita'
  "disabled = true"                       # botón bloqueado tras un envío no confirmado
  # --- ampliación 2026-11-08 (fix/contenido-embudo, comité CMO/CPO + orden CEO) ---
  'Powered by Trekko'                     # Trekko = marca hermana, no «powered by»
  'con la tecnolog.a de Trekko'
  'propuls. par Trekko'
  'technology partner'                    # ídem (relato de marca CEO 08-nov)
  'socio tecnol.gico'
  'partenaire technologique'
  'partner tecnologico'
  'the platform behind'
  'coming soon'                           # idiomas prometidos que no existen
  'pr.ximamente'
  'bient.t disponible'
  'prossimamente'
  '1M\+'                                  # cifra rancia: trekko.co publica 3M+
  'one million'
  'un mill.n'
  'un million'
  'un milione'
  'no third parties'                      # falso: operamos con proveedores
  'sin terceros'
  'sans tiers'
  'senza terzi'
  'no intermediaries'
  'sin intermediarios'
  'sans interm.diaire'
  'senza intermediari'
  'Mercedes fleet'                        # flota propia no acreditada
  'flota (propia|Mercedes)'
  'flotte (Mercedes|propre)'
  'flotta (Mercedes|propria)'
  'in-house'                              # exclusividad «todo en casa» no acreditada
  'en casa, con discreci'
  'en interne'
  'in casa, con discrezione'
  'Cairo'                                 # orden CEO 08-nov: fuera El Cairo
  'Le Caire'
  'Il Cairo'
  '\bArabic\b'                      # ni idioma árabe como servicio
  '(^|[^[:alpha:]])(á|a|Á|A)rabe([^[:alpha:]]|$)'
  '\barabo\b'
  # 'Middle East' / 'Oriente Medio' / 'Moyen-Orient' / 'Medio Oriente': RETIRADOS del candado
  # el 2026-11-08 por orden literal del CEO (D-2026-11-08-DMC-V2-CEO-AMPLIACION-Y-PUBLICAR:
  # «trusted DMC & tour operator for leading brands in the US, Europe, the Middle East and Latin America»).
  # Cairo / oficina en Oriente Medio / idioma árabe siguen PROHIBIDOS (arriba y abajo).
  '#1\b'                                 # superlativo no demostrable (matiz coordinador, mismo D-)
  'number one'
  'n[uú]mero uno'
  'numero uno'
  'num[eé]ro un\b'
  'n\.? ?º ?1\b'
  'n° ?1\b'
  '40\+'                                  # «40+ destinations» sin fuente
  '300\+'                                 # «300+ villas» sin fuente vigente
  'within 24'                             # SLA de respuesta no confirmado (N9)
  # --- v3 AEO 2026-11-08 (D-2026-11-08-DMC-V3-CEO-CLARIDAD-AEO): superlativos indemostrables ---
  'the best'
  'best DMC'
  'best tour operator'
  'el mejor (DMC|turoperador)'
  'le meilleur (DMC|tour-op)'
  'il miglior(e)? (DMC|tour operator)'
  # --- AR/RU/PT (2026-11-08, D-2026-11-08-DMC-IDIOMAS-AR-RU-PT-RANKING, gate cmo) ---
  'القاهرة'                               # El Cairo (AR)
  'رقم ?(1|١|واحد)'                       # «número 1» (AR)
  'أفضل'                                  # «el mejor» (AR) — superlativo vetado
  'الأفضل'
  'قريبا|قريبًا'                          # «coming soon» (AR)
  'باللغة العربية|نتحدث العربية|ناطق(ين)? بالعربية|سائق عربي|فريق عربي'   # no se ofrece atención en árabe
  'Каир'                                  # El Cairo (RU)
  'арабск|на арабском|арабоговорящ'       # árabe como idioma (RU)
  '№ ?1'                                  # «número 1» (RU)
  'номер один'
  'лучш'                                  # «el mejor» (RU)
  'скоро'                                 # «coming soon» (RU)
  'melhor'                                # «el mejor» (PT)
  'em breve'                              # «coming soon» (PT)
  'sem intermedi'                         # (PT)
  'frota pr.pria'                         # (PT)
)

# Términos prohibidos en el MARKETING pero obligatorios en las páginas legales
# (LSSI art. 10: domicilio social real). Se aplican a todo salvo /legal/ y /privacy/.
MARKETING_ONLY=(
  'Albacete'                              # orden CEO 08-nov: fuera de la página comercial
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

MKT_FILES=$(echo "$FILES" | grep -vE '^\./(legal|privacy)/')
for p in "${MARKETING_ONLY[@]}"; do
  hits=$(grep -inE -- "$p" $MKT_FILES 2>/dev/null)
  if [ -n "$hits" ]; then
    echo "FALLO — término comercial prohibido: /$p/"
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

if [ "$fail" -ne 0 ]; then
  echo
  echo "check-claims: NO PUBLICAR. Ver INSPECCIONES/2026-09-19-comite-dmc-cto.md §4."
  exit 1
fi

echo "check-claims: OK — $(echo "$FILES" | wc -l) locales, 0 claims retirados presentes."
exit 0

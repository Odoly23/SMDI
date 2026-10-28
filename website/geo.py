"""Koordenada aproximada sentru munisípiu Timor-Leste (ba peta impaktu iha homepage).
Chave = naran ho minúsculu no la iha asentu. Se naran iha database la hanesan, la hatudu iha mapa."""
import unicodedata

CENTROIDS = {
    "aileu": (-8.7289, 125.5662),
    "ainaro": (-9.0100, 125.5200),
    "atauro": (-8.2500, 125.5800),
    "baucau": (-8.4700, 126.4600),
    "bobonaro": (-8.9900, 125.2500),
    "covalima": (-9.2300, 125.2600),
    "dili": (-8.5586, 125.5736),
    "ermera": (-8.7500, 125.3980),
    "lautem": (-8.3700, 126.9000),
    "liquica": (-8.5900, 125.3400),
    "manatuto": (-8.5100, 126.0100),
    "manufahi": (-9.0000, 125.8000),
    "oecusse": (-9.3000, 124.3500),
    "viqueque": (-8.8600, 126.3600),
}
ALIASES = {"lautém": "lautem", "liquiçá": "liquica", "oe-cusse": "oecusse", "oecussi": "oecusse",
           "oecusse-ambeno": "oecusse", "ambeno": "oecusse", "raeoa": "oecusse"}


def _norm(name):
    s = unicodedata.normalize("NFKD", (name or "").strip().lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return ALIASES.get(name.strip().lower(), ALIASES.get(s, s))


def centroid_for(name):
    key = _norm(name)
    for k, v in CENTROIDS.items():
        if key == k or key.startswith(k):
            return v
    return None

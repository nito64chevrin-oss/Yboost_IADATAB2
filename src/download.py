"""Télécharge toutes les sources de données du projet dans data/raw/."""

from pathlib import Path

import requests

# Dossier de destination
RAW_DIR = Path("data") / "raw"

# Lien stable de téléchargement d'un fichier data.gouv.fr
DATAGOUV_DOWNLOAD_URL = "https://www.data.gouv.fr/api/1/datasets/r/{id}"

# Nom du fichier local -> URL de téléchargement
# (les jours fériés ne sont pas téléchargés : ils sont calculés dans prepare.py)
SOURCES = {
    "cnc_frequentation.xlsx": "https://www.data.gouv.fr/api/1/datasets/r/ecd520e1-b16d-4831-a5d7-586290d31e69",
}


def download_file(url: str, destination: Path) -> None:
    """Télécharge le fichier situé à `url` et l'enregistre dans `destination`."""
    print(f"Téléchargement de {destination.name}...")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    with open(destination, "wb") as f:
        f.write(response.content)

    taille_ko = destination.stat().st_size / 1024
    print(f"  -> OK ({taille_ko:.0f} Ko)")


# --- Vacances scolaires par zones (depuis 1990) ---

VACANCES_DATASET_ID = "5aeb1610c751df5402613fae"
VACANCES_API_URL = f"https://www.data.gouv.fr/api/1/datasets/{VACANCES_DATASET_ID}/"


def telecharger_vacances() -> None:
    """Retrouve le fichier CSV du jeu « Vacances scolaires par zones » et le télécharge."""
    response = requests.get(VACANCES_API_URL, timeout=60)
    response.raise_for_status()
    ressources = response.json()["resources"]

    # On cherche le fichier principal au format CSV
    for ressource in ressources:
        if ressource["type"] == "main" and "csv" in ressource["format"].lower():
            url = DATAGOUV_DOWNLOAD_URL.format(id=ressource["id"])
            download_file(url, RAW_DIR / "vacances_scolaires.csv")
            return

    raise RuntimeError("Aucun fichier CSV trouvé pour les vacances scolaires.")


# --- Météo-France : données quotidiennes ---

METEO_DATASET_ID = "6569b51ae64326786e4e8e1a"
METEO_API_URL = (
    f"https://www.data.gouv.fr/api/2/datasets/{METEO_DATASET_ID}"
    "/resources/?page=1&page_size=1000&type=main"
)

# Départements à télécharger (codes sur 2 chiffres)
DEPARTEMENTS = ["75", "13", "69", "59", "33", "31", "06", "44", "67", "34"]

# Périodes utiles pour couvrir 1993 -> aujourd'hui
PERIODES = ["periode_1950-2024", "periode_2025-2026"]


def lister_fichiers_meteo() -> list[dict]:
    """Interroge l'API data.gouv.fr et renvoie la liste de tous les fichiers du jeu de données."""
    response = requests.get(METEO_API_URL, timeout=60)
    response.raise_for_status()
    contenu = response.json()
    return contenu["data"]


def est_utile(titre: str) -> bool:
    """Renvoie True si le fichier concerne un de nos départements, la bonne période et RR-T-Vent."""
    bon_type = "RR-T-Vent" in titre
    bonne_periode = any(p in titre for p in PERIODES)
    bon_departement = any(f"departement_{d}_" in titre for d in DEPARTEMENTS)
    return bon_type and bonne_periode and bon_departement


def telecharger_meteo() -> None:
    """Télécharge les fichiers météo quotidiens des départements choisis."""
    meteo_dir = RAW_DIR / "meteo"
    meteo_dir.mkdir(parents=True, exist_ok=True)

    for fichier in lister_fichiers_meteo():
        titre = fichier["title"]
        if est_utile(titre):
            url = DATAGOUV_DOWNLOAD_URL.format(id=fichier["id"])
            download_file(url, meteo_dir / f"{titre}.csv.gz")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for nom_fichier, url in SOURCES.items():
        download_file(url, RAW_DIR / nom_fichier)

    telecharger_vacances()
    telecharger_meteo()

    print("Toutes les données ont été téléchargées.")


if __name__ == "__main__":
    main()
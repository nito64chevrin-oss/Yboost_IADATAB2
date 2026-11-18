from pathlib import Path

import requests

RAW_DIR = Path("data") / "raw"

SOURCES = {
    "cnc_frequentation.xlsx": "https://www.data.gouv.fr/api/1/datasets/r/ecd520e1-b16d-4831-a5d7-586290d31e69",
    "calendrier_scolaire.csv": "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-calendrier-scolaire/exports/csv",
    "jours_feries.csv": "",  # à compléter : lien du CSV sur data.gouv.fr
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


METEO_DATASET_ID = "6569b51ae64326786e4e8e1a"
METEO_API_URL = (
    f"https://www.data.gouv.fr/api/2/datasets/{METEO_DATASET_ID}"
    "/resources/?page=1&page_size=1000&type=main"
)

DATAGOUV_DOWNLOAD_URL = "https://www.data.gouv.fr/api/1/datasets/r/{id}"

DEPARTEMENTS = ["75", "13", "69", "59", "33", "31", "06", "44", "67", "34"]

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
        if not url:
            print(f"Lien manquant pour {nom_fichier}, fichier ignoré.")
            continue
        download_file(url, RAW_DIR / nom_fichier)

    telecharger_meteo()

    print("Toutes les données ont été téléchargées.")


if __name__ == "__main__":
    main()
import pandas as pd

cnc = pd.read_excel(
    "../data/raw/cnc_frequentation.xlsx",
    sheet_name="semaine",
    skiprows=6,
    nrows=54,
)
cnc = cnc.rename(columns={"Entrées (millions)": "semaine"})

# --- Passage au format long : une ligne par semaine ---
cnc_long = cnc.melt(id_vars="semaine", var_name="annee", value_name="entrees")

# --- Nettoyage ---
cnc_long["semaine"] = cnc_long["semaine"].str.extract(r"(\d+)")[0].astype(int)
cnc_long["annee"] = cnc_long["annee"].astype(int)
cnc_long = cnc_long[cnc_long["semaine"].between(1, 52)]        # retire les semaines 0 et 53
cnc_long = cnc_long.dropna(subset=["entrees"])                  # retire les cases vides
cnc_long = cnc_long[~cnc_long["annee"].isin([2020, 2021])]      # retire les années Covid
cnc_long["entrees"] = cnc_long["entrees"].astype(int)
cnc_long = cnc_long.sort_values(["annee", "semaine"]).reset_index(drop=True)

MERCREDI = 2  # pandas numérote les jours de lundi = 0 à dimanche = 6


def dates_semaine(annee: int, semaine: int) -> pd.Series:
    """Renvoie la date de début, la date de fin et le nombre de jours d'une semaine CNC.

    Une semaine de cinéma va du mercredi au mardi, et ne dépasse jamais
    le 1er janvier ni le 31 décembre.
    """
    premier_janvier = pd.Timestamp(year=annee, month=1, day=1)

    # Premier mercredi de l'année (le 1er janvier lui-même s'il tombe un mercredi)
    decalage = (MERCREDI - premier_janvier.dayofweek) % 7
    premier_mercredi = premier_janvier + pd.Timedelta(days=decalage)

    # Si le 1er janvier tombe un jeudi, vendredi ou samedi,
    # les jours avant le premier mercredi forment une semaine 1 incomplète
    semaine1_incomplete = premier_janvier.dayofweek in (3, 4, 5)

    if semaine1_incomplete and semaine == 1:
        debut = premier_janvier
        fin = premier_mercredi - pd.Timedelta(days=1)
    elif semaine1_incomplete:
        debut = premier_mercredi + pd.Timedelta(weeks=semaine - 2)
        fin = debut + pd.Timedelta(days=6)
    else:
        debut = premier_mercredi + pd.Timedelta(weeks=semaine - 1)
        fin = debut + pd.Timedelta(days=6)

    # Une semaine ne dépasse jamais le 31 décembre
    fin = min(fin, pd.Timestamp(year=annee, month=12, day=31))

    nb_jours = (fin - debut).days + 1
    return pd.Series({"date_debut": debut, "date_fin": fin, "nb_jours": nb_jours})


cnc_long[["date_debut", "date_fin", "nb_jours"]] = cnc_long.apply(
    lambda ligne: dates_semaine(ligne["annee"], ligne["semaine"]), axis=1
)

cnc_long = cnc_long[cnc_long["nb_jours"] == 7].reset_index(drop=True)

cnc_long.shape
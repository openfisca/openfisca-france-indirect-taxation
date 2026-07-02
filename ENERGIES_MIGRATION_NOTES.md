# Energy-tax parameter migration into OFFIT — working notes

**Status:** analysis complete, implementation NOT started. Paused on one open domain
decision (see §6). Safe to resume from any machine by reading this file.

**Branch:** `energies_migration` (this file is the only change so far).

## 1. Goal

Import the energy-tax legislation overhaul from **baremes-ipp-yaml** (branch `energies`,
tree `parameters/taxation_indirecte/energies/`) into **OFFIT**, replacing OFFIT's two
current subtrees:

- `parameters/imposition_indirecte/produits_energetiques/`
- `parameters/imposition_indirecte/taxes_energie_dans_logement/`

…**without breaking the model**. The two repos track each other but sync is manual/patchy.

### Decisions already made
- **Target location in OFFIT:** `parameters/imposition_indirecte/energies/` — keep OFFIT's
  existing top-level namespace `imposition_indirecte`, adopt the new internal structure.
  (So references become `parameters(period).imposition_indirecte.energies.*`.)
- **Scope:** rewire ALL Python consumers (preprocessing + variables + reforms) so the
  model runs, not just the YAML swap.

## 2. How OFFIT's parameter system works (context)

- Loaded in `openfisca_france_indirect_taxation/france_indirect_taxation_taxbenefitsystem.py`
  via `self.load_parameters(param_dir)` over the whole `parameters/` folder.
- **The directory tree IS the API.** A file
  `parameters/imposition_indirecte/produits_energetiques/accise_energie_metropole/essences.yaml`
  is read in code as
  `parameters(period).imposition_indirecte.produits_energetiques.accise_energie_metropole.essences`.
  Renaming a folder/file = breaking every reference to it.
- After loading, `__init__` runs `preprocess_legislation(self.parameters)`
  (`parameters/preprocessing.py`). Two energy-relevant things it does:
  1. Builds HT fuel prices (`prix_carburants`) for years 2011→now. **Branches on
     `year >= 2022`:** post-2022 reads `accise_energie_metropole.*` (€/MWh) × a
     `taux_conversion_*` factor; pre-2022 reads `ticpe.*` (€/hL).
     Formula: `calculate_ht_price = ttc/(1+tva) − (ticpe + majoration_regionale − (maximum_value_affectation − affectation_regionale))`.
  2. Lines ~716–724: converts pre-2002 values from francs→euros (`/6.55957`) by iterating
     `produits_energetiques.ticpe.children`.

## 3. The core finding: divergence is in THREE distinct buckets

A straight "delete old / drop in new" **silently breaks the model**. The trees differ in
three ways:

### Bucket ① — Core accise & TICPE: same concept, moved + renamed (safe to rewire)
Values match and the new tree **preserves full pre-2022 history including pre-2002 francs**
(e.g. new `ticpe/huiles_legeres/super/super_e5.yaml` has 1993→2018, francs before 2002),
so `preprocessing.py`'s francs→euros conversion still applies unchanged. Just needs path
rewiring in code. **Value spot-checks done:** essences 76.826 = 76.826 ✓; gazoles 59.4.

### Bucket ② — OFFIT-only parameters, ABSENT from baremes (MUST be carried over)
No equivalent exists in the new tree. If deleted, the model breaks:
- `taux_conversion_euro_par_mwh_a_euro_par_hectolitre` (MWh→hL factors used by
  `preprocessing.py` and `accise_ticpe_carburants.py`)
- `affectation_regionale_ticpe_{gazole,sp95_e10,sp95_sp98}` (incl. `maximum_value_affectation`
  and region code `["99"]`)
- `refraction_corse_ticpe`
- `majoration_ile_de_france_mobilites_ticpe`
- `aide_exceptionnelle_carburant`

### Bucket ③ — Present in both but INCOMPATIBLE (structure AND values differ) — **UNRESOLVED**
- `majoration_regionale_ticpe_gazole` and `majoration_regionale_ticpe_sp95_sp98_sp95_e10`
  (super). See §6 for the detailed diff and why this is the open decision.
- `tgap_carburants`: structurally compatible (`.super_95` works either way); only a tiny
  2019 tweak (old `0.079` → new `null`); **appears unused by current OFFIT variables** →
  low risk. Confirm no reform depends on the 2019 value before swapping.

## 4. Old → new path mapping (base for Bucket ①)

New base path = `imposition_indirecte.energies.autres_produits_energetiques.metropole`.
Entries marked **(VERIFY)** were inferred from names, not yet value-checked leaf-by-leaf.

| Old OFFIT path (under `imposition_indirecte.produits_energetiques`) | New path (under `…energies.autres_produits_energetiques.metropole`) |
|---|---|
| `accise_energie_metropole.essences` | `accise.carburants.huiles_legeres.essences` ✓ |
| `accise_energie_metropole.gazoles` | `accise.carburants.huiles_lourdes.gazoles` ✓ |
| `accise_energie_metropole.essence_sp95_e10` | `accise.carburants.tarifs_particuliers.essence_sp95_e10` (VERIFY) |
| `accise_energie_metropole.superethanol_e85` | `accise.carburants.tarifs_particuliers.superethanol_e85` (VERIFY) |
| `accise_energie_metropole.gpl_carburant` | `accise.carburants.hydrocarbures_gazeux_liquefies.gaz_petrole_liquefies` (VERIFY) |
| `ticpe.gazole` (B7) | `ticpe.huiles_lourdes.gazole.gazole_autres` (VERIFY — confirm B7 vs autres) |
| `ticpe.gazol_b_10_hectolitre` | `ticpe.huiles_lourdes.gazole.gazole_b_10` (VERIFY) |
| `ticpe.gazole_fioul_domestique_hectolitre` | `ticpe.huiles_lourdes.gazole.fioul_domestique` (VERIFY) |
| `ticpe.super_e10` | `ticpe.huiles_legeres.super.super_e10` (VERIFY) |
| `ticpe.super_95_98` | `ticpe.huiles_legeres.super.super_e5` ✓ (desc "Supercarburants dont SP95 et SP98") |
| `ticpe.super_plombe` | `ticpe.huiles_legeres.super.super_plombe` (VERIFY) |
| `ticpe.super_e_85_utilise_comme_carburant_hectolitre` | `ticpe.super_e85` (VERIFY) |
| `ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants_autres_100kg` | `ticpe.propanes_butanes_etc.autres_gaz_petrole_liquefies_utilises_comme_carburants.autres` (VERIFY — units: old is /100kg) |
| `tgap_carburants.<fuel>` | `tgap_carburants.<fuel>` (dir now; 2019 value differs) |

**Housing energy (`taxes_energie_dans_logement`)** — only used in
`projects/budgets/reforme_energie_budgets_2018_2019.py`:
| Old | New |
|---|---|
| `taxes_energie_dans_logement.taxes_electricite_et_gaz.ticgn_prix_par_mwh` | `energies.gaz_naturel.ticgn.taux_normal` (VERIFY units/value) |

The rest of the new tree (`electricite/` with cspe/cta/tcfe/ticfe, `gaz_naturel/` with
cspg/ctssg/ticgn detail, `charbon/`, `drom/`, dozens of `tarifs_reduits/`) is **new detail
OFFIT doesn't currently model** — importing it is harmless (extra params don't break
anything) and is part of adopting the overhaul.

## 5. Code consumers to rewire (grep-verified)

Old `produits_energetiques.*` references:
- `parameters/preprocessing.py` (HT price build + francs conversion loop)
- `variables/taxes_indirectes/accise_ticpe_carburants.py` (heaviest — ~60 references)
- `variables/taxes_indirectes/prix_carburants_ht.py`
- `variables/taxes_indirectes/prix_carburants_ttc.py`
- `variables/taxes_indirectes/prix_carburants_ttc_sortie.py`
- `variables/taxes_indirectes/ticpe_combustibles_liquides.py`
- `variables/taxes_indirectes/__init__.py`
- `reforms/`: `taxe_carbone.py`, `rattrapage_diesel.py`, `officielle_2018_in_2016.py`,
  `officielle_2019_in_2018.py`, `cce_2015_in_2014.py`, `cce_2016_in_2014.py`
- project scripts/notebooks (lower priority): `projects/PhD_project_Herve/`,
  `projects/Master_Thesis_Herve/`, `projects/budgets/reforme_energie_budgets_2018_2019.py`

Old `taxes_energie_dans_logement.*` references: only
`projects/budgets/reforme_energie_budgets_2018_2019.py` (lines ~1040, 1053).

Note: region code `"99"` = "France / default when region unspecified"; also used in
`prix_carburants_ttc.py` as a sentinel (`region_cell == "99"`) — unrelated to the parameter
node but be careful not to conflate the two when refactoring.

## 6. OPEN DECISION — regional majorations (Bucket ③)

**This is what to resolve next, after re-reading the legislation on the baremes side.**

The regional majoration diff (gazole, €/hL) shows the two trees encode the tax differently:

| Region | Year | OFFIT (code-keyed) | Baremes (name-keyed) |
|---|---|---|---|
| Île-de-France | 2012 | 1.35 | 2.5 |
| | 2017 | 1.35 | **4.39** |
| | 2022 | 1.35 (€/MWh) | — (none) |
| Rhône-Alpes | 2014 | 1.35 | 2.5 |
| | 2017 | **null** (dissolved) | 2.5 (still live) |
| Corse | 2017 | 0.0 | 1.15 |

**Key insight — baremes CONSOLIDATES what OFFIT splits into three parameters:**
- OFFIT keeps `majoration_regionale` (≈1.35 cap) **+** `affectation_regionale` (≤1.15, with
  `maximum_value_affectation`) **+** `majoration_ile_de_france_mobilites` — separate nodes,
  and the HT-price formula depends on the split.
- Baremes folds them into one per-region number: 1.35 + 1.15 ≈ **2.5**, and IdF's **4.39**
  = 2.5 + the Mobilités surcharge.

Other differences: baremes covers 2007→2017 (no post-2022 €/MWh values here); OFFIT covers
2011-07→2022. After the 2016 territorial reform OFFIT nulls old regions and switches to
new-region codes, baremes keeps pre-reform regions live.

**Implication:** adopting baremes here is NOT a drop-in. It requires deleting
`affectation_regionale` + `maximum_value_affectation` + `majoration_ile_de_france_mobilites`,
**re-deriving the HT-price formula** in `preprocessing.py` and `accise_ticpe_carburants.py`,
switching region indexing from INSEE codes to names, dealing with the missing post-2022
values, **and it changes model results**.

### The two options on the table
- **(Recommended) Preserve OFFIT's version:** carry OFFIT's code-keyed
  `majoration_regionale` + `affectation_regionale` + `maximum_value_affectation` +
  `majoration_ile_de_france_mobilites` into the new tree unchanged; import everything else
  from baremes. Model results unchanged, formula untouched.
- **Adopt baremes' consolidated version:** full sync, but changes results and needs the
  formula/region-indexing rewrite described above.

User decision (2026-07): deferred — needs more work on the baremes side (re-read the
legislation on how the consolidated majoration is defined) before choosing. Revisit then.

## 7. Recommended implementation plan (once Bucket ③ is decided)

1. Copy the full baremes `energies/` tree into
   `parameters/imposition_indirecte/energies/`; delete `produits_energetiques/` and
   `taxes_energie_dans_logement/`.
2. Carry Bucket ② (and, per §6 decision, possibly Bucket ③) OFFIT-only nodes into the new
   tree at sensible sub-paths.
3. Verify every Bucket ① leaf mapping in §4 by value (write a small script that loads both
   trees and diffs the leaves the code touches). Resolve all **(VERIFY)** rows.
4. Rewire `preprocessing.py`, the 5 `variables/taxes_indirectes/*` files, and the reforms.
5. Verify: build the TaxBenefitSystem (import
   `FranceIndirectTaxationTaxBenefitSystem`), run the test suite (`tests/`), and diff key
   variable outputs (accise TICPE per fuel, prix HT/TTC) against `master`.

## 8. Reference paths
- OFFIT: `c:/Users/p.dutronc/Documents/projets/openfisca-france-indirect-taxation`
- baremes-ipp-yaml: `c:/Users/p.dutronc/Documents/projets/baremes-ipp-yaml` (branch `energies`)
- New tree: `baremes-ipp-yaml/parameters/taxation_indirecte/energies/`

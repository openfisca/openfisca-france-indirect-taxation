Ce document donne des exemples d'utilisation, centrés sur la TVA, qui couvrent à la fois des simulations d'un système socio-fiscal et une simulation de réforme.

# Simuler la TVA actuelle 

```
from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.utils import get_input_data_fram
from openfisca_france_indirect_taxation.Calage_consommation_bdf import get_inflators_by_year
from openfisca_france_indirect_taxation.Calage_revenus_bdf import calage_bdf_niveau_vie

data_year = 2017
year = 2024
tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
inflators_by_year = get_inflators_by_year(rebuild = False, year_range = range(2017, 2025), data_year = data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
```

La première étape de la simulation consiste à choisir le système socio-fiscal (`tax_benefit_system`) que l'on souhaite utiliser. On récupère celui défini par `FranceIndirectTaxationBenefitSystem()` que l'on a importé au préalable. On crée également le dictionnaire à utiliser dans la simulation pour caler/viellir les données de consommation (`inflation_kwargs`). Pour caler/veillir les revenus (et niveaux de vie), il y a deux possibilités :

**Option 1: Utiliser une source externe (ici TaxIPP).**
On utilise une dataframe qui donne les niveaux de vie moyen par dixième dans TaxIPP pour l'année de simulation (ici 2024). La dataframe est indexée par 'decile_indiv_niveau_vie' et contient une colonne 'niveau_de_vie'.
```
input_bdf = get_input_data_frame(2017)
input_bdf = input_bdf.loc[input_bdf['rev_disponible'] > 0]
input_bdf , df_calage = calage_bdf_niveau_vie(input_bdf, decile_taxipp)
```

**Option 2: Utiliser l'ERFS.**
On appelle une fonction qui crée directement la dataframe souhaitée à partir des données de l'ERFS. Le reste est identique.
```
input_bdf = get_input_data_frame(2017)
input_bdf = input_bdf.loc[input_bdf['rev_disponible'] > 0]
erfs_path = 'C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Data/erfs_fpr/2017/csv' 
decile_erfs = compute_erfs_decile(2017,erfs_path)
input_bdf , df_calage = calage_bdf_niveau_vie(input_bdf, decile_erfs)
```

Une fois défini le `tax_benefit_system`, on peut faire tourner le code suivant, qui crée l'objet que l'on appelle `survey_scenario`:
```
survey_scenario = SurveyScenario.create(
    input_data_frame = input_bdf,
    inflation_kwargs =  inflation_kwargs,
    tax_benefit_system = tax_benefit_system,
    year = year
    ) 
```

Voir la documentation précise de la méthode `create` de la classe `SurveyScenario` dans la [section dédiée](Survey_scenario.md), avec notamment les autres arguments de cette fonction. <br>
La fonction applique le `tax_benefit_system` aux données de la [base d'entrée](../Donnees/Construction.md) pour une année `year`. Il est important de noter que le *survey scenario* est défini pour une année précise (paramètre `year`). Les résultats calculés à partir du *survey scenario* ne sont valables que pour cette année-là car les données ont été calibrées pour cette année-là. Cette vigilence est à garder en tête, particulièrement dans le cas de l'utilisation de méthodes associées au *survey scenario* et présentées dans les section suivante.

## Manipulation du Survey Scenario

Maintenant que l'on dispose d'une simulation de la fiscalité indirecte pour l'année 2024, via le `survey_scenario`. On peut procéder à quelques manipulations.

```
simulated_variables = ['depenses_tva_taux_plein',
'depenses_tva_taux_intermediaire',
'depenses_tva_taux_reduit',
'depenses_tva_taux_super_reduit',
'depenses_tot'
'depenses_tot',
'tva_total',
'rev_disponible',
'niveau_de_vie',
'niveau_vie_decile',
'pondmen',
'identifiant_menage']

baseline_menage = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
```
La fonction `create_data_frame_by_entity` permet d'obtenir les résultats de la simulation pour une liste de variables. Si plusieurs entités sont définis dans le *survey scenario*, cette fonction crée autant de dataframes que d'entités, il faut donc choisir la table 'menage' pour avoir les résultats par ménage.

```
tva_total = survey_scenario.compute_aggregate(variable='tva_total', use_baseline = False,  period = year)
```

La méthode `compute_aggregate` permet de calculer la masse agrégée d'une variable du `tax_benefit_system` pour une `period` donnée, ici en l'occurence les montants de TVA collectés (le montant total ainsi que sa ventilation dans les différents taux). <br>

# Simuler une réforme de la TVA 

Pour simuler les effets d'une réforme, il faut créer un *survey scenario* avec deux systèmes socio-fiscaux : un système avant réforme, défini par l'argument `baseline_tax_benefit_system` et un système après réforme, défini par l'argument `tax_benefit_system`. 

## Coder une réforme 

Il est aussi possible de définir le système après-réforme comme le résultat d'une fonction (la réforme) appliquée au sytème de référence. Dans ce cas, on peut utiliser l'argument `reform`.

``` 
from openfisca_core.reforms import Reform
from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore

def reform_modify_parameters(baseline_parameters_copy):
    reform_parameters = baseline_parameters_copy
    
    node = ParameterNode(
    'augmentation_tva_2025',
    data = {
        "description": 'augmentation_tva_2025',
        "delta_taux": {
            "description": "Augmentation d'un point de TVA",
            "unit": '/1',
            "values": {'2024-01-01': 0.01}
            },
        }
    )
    reform_parameters.imposition_indirecte.tva.taux_de_tva.add_child('augmentation_tva_2025', node)
    return reform_parameters

class augmente_tous_les_taux(Reform):
    name = u'Augmentation de tous les taux de TVA (+1 p.p.)'
    
    class depenses_tva_taux_plein(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux plein"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_plein = menage('depenses_ht_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux
            
            return depenses_ht_tva_taux_plein * (1 + taux_plein + augmentation)
    
    class tva_taux_plein(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux plein"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_plein = menage('depenses_ht_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux
            
            return depenses_ht_tva_taux_plein * (taux_plein + augmentation)

    class depenses_tva_taux_intermediaire(YearlyVariable):  
    ...
          
    def apply(self):
        self.update_variable(self.depenses_tva_taux_plein)
        self.update_variable(self.tva_taux_plein) 
        self.update_variable(self.depenses_tva_taux_intermediaire)
        self.update_variable(self.tva_taux_intermediaire)
        self.update_variable(self.depenses_tva_taux_reduit)
        self.update_variable(self.tva_taux_reduit)         
        self.update_variable(self.depenses_tva_taux_super_reduit)
        self.update_variable(self.tva_taux_super_reduit)        
        self.modify_parameters(modifier_function = reform_modify_parameters)```
```

Dans l'exemple ci-dessus on a codé la réforme `augmente_tous_les_taux` qui augmente les taux de TVA d'un point de pourcentage. Plus techniquement, cette fonction utilise la fonction  `reform_modify_parameters` qui prend en argument les paramètres d'un *tax benefit system* et y ajoute un nouveau paramètre qui correspond à l'augmentation. On peut ensuite redéfinir les variables `depenses_tva_taux_...` et `tva_taux_...` sur le modèle des variables qui se rapportent au taux plein.

```
survey_scenario = SurveyScenario.create(
    input_data_frame = input_bdf,
    inflation_kwargs =  inflation_kwargs,
    baseline_tax_benefit_system = tax_benefit_system,
    reform = augmente_tous_les_taux,
    year = year
    )
```

L'argument `reform = augmente_tous_les_taux` définit implicitement le système réformé  comme suit : `tax_benefit_system = augmente_tous_les_taux(baseline_tax_benefit_system)`.

### Calcul des dépenses hors-taxes

Pour chaque taux de TVA, une variable `depenses_ht_tva_taux_...` est calculée en sommant toutes les variables `depense_ht_poste_...` de tous les postes soumis au taux en question.
Pour chacun des postes, une variable `depense_ht_poste_` est calculée en retirant la TVA aux dépenses TTC, à l'aide de la fonction `generate_depenses_ht_postes_variables()`.<br>
Il est important de noter que le SurveyScenario utilise les paramètres définis dans le système socio-fiscal (de base ou réformé) pour effectuer ce calcul. Ainsi, **un système dont on a changé les taux de TVA prend en compte ces nouveaux taux pour calculer les dépenses hor-taxes, ce qui aboutit à avoir des dépenses hors-taxes différentes entre la baseline et le système réformé.**

## Mesurer les effets d'une réforme 

```
tva_total_reform = survey_scenario.compute_aggregate(variable ='tva_total', use_baseline = False, period = year)
delta_total = survey_scenario.compute_aggregate(variable ='tva_total', difference = True, period = year)
```
Tout comme de nombreuses autres méthodes, la méthode `compute_aggregate` contient un argument `use_baseline`, qui vaut True ou False (avec False comme valeur par défaut). Tout *survey scenario* contient parmi ses attributs soit un `tax_benefit_system`, soit, en cas d'analyse de réforme, à la fois un `tax_benefit_system` et un `baseline_tax_benefit_system`. Si `use_baseline = True`, cela veut dire que l'on souhaite un résultat pour le  `baseline_tax_benefit_system`, et inversement. Il est également possible de faire la différence entre les variables sous le système réformé et le système de référence, en utilisant l'argument `difference = True`. Dans l'exemple ci-dessus, on peut mesurer l'effet d'une augmentation d'un point de TVA sur les montants collectés par taux et total.
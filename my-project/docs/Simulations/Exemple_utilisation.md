Ce document donne des exemples d'utilisation, centrés sur la TVA, qui couvrent à la fois des simulations d'un système socio-fiscal et une simulation de réforme.

# Simuler la TVA actuelle 

```
from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.projects.TVA_Herve_IPP.new_calage_bdf_cn import new_get_inflators_by_year

data_year = 2017
year = 2024
tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
inflators_by_year = new_get_inflators_by_year(rebuild = False, year_range = range(2017, 2025), data_year = data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
```

La première étape de la simulation consiste à choisir le système socio-fiscal (`tax_benefit_system`) que l'on souhaite utiliser. On récupère celui défini par `FranceIndirectTaxationBenefitSystem()` que l'on a importé au préalable. On crée également le dictionnaire à utiliser pour caler/viellir les données (`inflation_kwargs`). 

Une fois défini le `tax_benefit_system`, on peut faire tourner le code suivant, qui crée l'objet que l'on appelle `survey_scenario`:
```
survey_scenario = SurveyScenario.create(
    inflation_kwargs =  inflation_kwargs,
    baseline_tax_benefit_system = tax_benefit_system,
    year = year,
    data_year = data_year
    ) 
```

Voir la documentation précise de la méthode `create` de la classe `SurveyScenario` dans la [section dédiée](Survey_scenario.md), avec notamment les autres argmuents de cette fonction. <br>
La fonction applique le `tax_benefit_system` aux données de la [base d'entrée](../Donnees/Construction.md) pour une année `year`. Il est important de noter que le *survey scenario* est défini pour une année précise (paramètre `year`). Les résultats calculés à partir du *survey scenario* ne sont valables que pour cette année-là car les données ont été calibrées pour cette année-là. Cette vigilence est à garder en tête, particulièrement dans le cas de l'utilisation de méthodes associées au *survey scenario* et présentées dans les section suivante. En effet, la plupart de ces fonctions ont un paramètre `period` à définir. Il est donc important de n'utiliser ces fonctions que pour des périodes correspondantes à l'année `year`. 

## Manipulation du Survey Scenario

Maintenant que l'on dispose d'une simulation de la fiscalité indirecte pour l'année 2024, via le `survey_scenario`. On peut procéder à quelques manipulations.

```
tva_total = survey_scenario.compute_aggregate(variable='tva_total', use_baseline = False,  period = year)
taux_plein = survey_scenario.compute_aggregate(variable='tva_taux_plein', use_baseline = False, period = year)
taux_intermediaire = survey_scenario.compute_aggregate(variable='tva_taux_intermediaire', use_baseline = False, period = year)
taux_reduit = survey_scenario.compute_aggregate(variable='tva_taux_reduit', use_baseline = False, period = year)
taux_super_reduit = survey_scenario.compute_aggregate(variable='tva_taux_super_reduit', use_baseline = False, period = year)
```

La méthode `compute_aggregate` permet de calculer la masse agrégée d'une variable du `tax_benefit_system` pour une `period` donnée, ici en l'occurence les montants de TVA collectés (le montant total ainsi que sa ventilation dans les différents taux). <br>
Tout comme de nombreuses autres méthodes, la méthode `compute_aggregate` contient un argument `use_baseline`, qui vaut True ou False (avec False comme valeur par défaut). Tout survey scenario contient parmi ses attributs soit un `tax_benefit_system`, soit, en cas d'analyse de réforme, à la fois un `tax_benefit_system` et un `baseline_tax_benefit_system`. Si `use_baseline = True`, cela veut dire que l'on souhaite un résultat pour le  `baseline_tax_benefit_system`, et inversement. Or, ici, on n'a qu'un seul système de défini. Ce seul système , est mis - s'il n'y a qu'un seul système - dans l'attribut `tax_benefit_system` du *survey scenario*  (cette opération est faite dans la méthode create du fichier `scenario.py`), d'où le fait qu'il faille spécifier ici `use_baseline = False`, ce qui n'est pas nécessaire, étant donné qu'il s'agit de l'option par défaut.

```
simulated_variables = ['depenses_tva_taux_plein',
'depenses_tva_taux_intermediaire',
'depenses_tva_taux_reduit',
'depenses_tva_taux_super_reduit',
'depenses_tot']

means_by_decile = dataframe_by_group(survey_scenario, 
    category = 'niveau_vie_decile', 
    variables = simulated_variables, 
    aggfunc = 'mean')
```

La fonction `dataframe_by_group` permet, à partir d'un `survey_scenario` donné en argument, de construire une dataframe agrégée (ici par décile de niveau de vie) qui contient les variables choisies. La fonction d'agrégation définie dans l'argument `aggfunc` est ici la moyenne (cela peut aussi être une somme). Dans l'exemple ci-dessus, la dataframe construite contient par décile de niveau de vie les dépenses moyennes des ménages (totales ou par type de taux de TVA).

# Simuler une réforme de la TVA 

Pour simuler les effets d'une réforme, il faut créer un *survey scenario* avec deux systèmes socio-fiscaux : un système avant réforme, défini par l'argument `baseline_tax_benefit_system` et un système après réforme, défini par l'argument `tax_benefit_system`. 

## Coder une réforme 

Il est aussi possible définir le système après-réforme comme le résultat d'une fonction (la réforme) appliquée au sytème de référence. Dans ce cas, on peut utiliser l'argument `reform`.

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

Dans l'exemple ci-dessus on a codé la réforme `augmente_tous_les_taux` qui augmente les taux de TVA d'un point de pourcentage. Plus techniquement, cette fonction utilise la fonction  `reform_modify_parameters` qui prend en argument les paramètres d'un *tax benefit system* et y ajoute un nouveau paramètre qui correspond à à l'augmentation. On peut ensuite redéfinir les variables `depenses_tva_taux_...` et `tva_taux_...` sur le modèle des variables qui se rapportent au taux plein.

```
survey_scenario = SurveyScenario.create(
    inflation_kwargs =  inflation_kwargs,
    baseline_tax_benefit_system = tax_benefit_system,
    reform = augmente_tous_les_taux,
    year = year,
    data_year = data_year
    )
```

L'argument `reform = augmente_tous_les_taux` définit implicitement le système réformé  comme suit : `tax_benefit_system = augmente_tous_les_taux(baseline_tax_benefit_system)`.

### Calcul des dépenses hors-taxes

Pour chaque taux de TVA, une variable `depenses_ht_tva_taux_...` est calculée en somme toutes les variables `depense_ht_poste_...` de tous les postes soumis au taux en question.
Pour chacun des postes, une variable `depense_ht_poste_` est calculée en retirant la TVA aux dépenses TTC, à l'aide de la fonction `generate_depenses_ht_postes_variables()`.<br>
Il est important de noter que le SurveyScenario utilise les paramètres définis dans le système socio-fiscal (de base ou réformé) pour effectuer ce calcul. Ainsi, **un système dont on a changé les taux de TVA prend en compte ces nouveaux taux pour calculer les dépenses hor-taxes, ce qui abouti à avoir des dépenses hors-taxes différentes entre la baseline et le système réformé.**

## Mesurer les effets d'une réforme 

```
delta_total = survey_scenario.compute_aggregate(variable ='tva_total', difference = True, period = year)
delta_taux_plein = survey_scenario.compute_aggregate(variable ='tva_taux_plein', difference = True, period = year) 
delta_taux_inter = survey_scenario.compute_aggregate(variable ='tva_taux_intermediaire', difference = True, period = year)
delta_taux_reduit = survey_scenario.compute_aggregate(variable ='tva_taux_reduit', difference = True, period = year)
delta_taux_super_reduit = survey_scenario.compute_aggregate(variable ='tva_taux_super_reduit', difference = True, period = year)
```

Pour la méthode `compute_aggregate`, comme pour d'autres méthodes, il est possible de faire directement la différence entre les variables sous le système réformé et le système de référence, en utilisant l'argument `difference = True`. Dans l'exemple ci-dessus, on peut mesurer l'effet d'une augmentation d'un point de TVA sur les montants collectés par taux et total.
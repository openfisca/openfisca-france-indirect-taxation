from importlib import metadata

openfisca_france_indirect_taxation_location = metadata.distribution('openfisca-france-indirect-taxation').files[0].locate().parent

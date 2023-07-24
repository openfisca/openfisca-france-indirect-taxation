from importlib import metadata
from pathlib import Path

openfisca_france_indirect_taxation_location = Path(
    metadata.distribution('openfisca-france-indirect-taxation').files[0]
    ).parent

# -*- coding: utf-8 -*-

import argparse
import configparser
import datetime
import logging
import os
import pkg_resources
import sys


from openfisca_survey_manager.scripts.build_collection import build_survey_collection

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)

raw_data_ini = os.path.join(
    pkg_resources.get_distribution('openfisca_survey_manager').location,
    'raw_data.ini'
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', default = raw_data_ini, help = "path of configuration file", nargs = '?')
    parser.add_argument(
        '-c', '--collection',
        help = "name of collection to build or update ('budget_des_familles', 'aliss' or 'both')",
        choices = ['aliss', 'both', 'budget_des_familles'],
        default = 'both',
        )
    parser.add_argument('-d', '--replace-data', action = 'store_true', default = True,
        help = "erase existing survey data HDF5 file (instead of failing when HDF5 file already exists)")
    parser.add_argument('-m', '--replace-metadata', action = 'store_true', default = True,
        help = "erase existing collection metadata JSON file (instead of just adding new surveys)")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    config_parser = configparser.SafeConfigParser()
    config_parser.read(args.config)

    if args.collection == 'both':
        assert config_parser.has_section(args.collection), 'aliss'
        assert config_parser.has_section(args.collection), 'budget_des_familles'
        collections = ['aliss', 'budget_des_familles']
    else:
        assert config_parser.has_section(args.collection), 'Unkwnown collection'
        collections = [args.collection]

    data_directory_path_by_survey_suffix = dict(config_parser.items(args.collection))

    start_time = datetime.datetime.now()

    for collection in collections:
        build_survey_collection(
            collection_name = collection,
            data_directory_path_by_survey_suffix = data_directory_path_by_survey_suffix,
            replace_metadata = args.replace_metadata,
            replace_data = args.replace_data,
            source_format = 'sas',
            )

    log.info("The program has been executed in {}".format(datetime.datetime.now() - start_time))

    return 0


if __name__ == "__main__":
    sys.exit(main())

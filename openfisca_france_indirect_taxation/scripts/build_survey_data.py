"""Build survey data."""


import argparse
import datetime
import logging
try:
    import ipdb as pdb
except ImportError:
    import pdb
import os
import sys


from openfisca_france_indirect_taxation.build_survey_data.run_all import run


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def main():
    parser = argparse.ArgumentParser()
    all_years = [2011, 2017]
    parser.add_argument('-y', '--years', nargs='+', help = "years of survey to build (default = {})'".format(all_years), default = all_years)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    parser.add_argument('-p', '--pdb', action = 'store_true', default = False, help = "use python debugger")
    parser.add_argument('-s', '--skip-matching', action = 'store_true', default = False, help = "skip matching step")

    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    start_time = datetime.datetime.now()
    years_calage = [int(year) for year in args.years]

    try:
        run(years_calage, skip_matching = args.skip_matching)
    except Exception as e:
        if args.pdb:
            pdb.post_mortem(sys.exc_info()[2])
        raise e

    log.info("The program has been executed in {}".format(datetime.datetime.now() - start_time))
    return 0


if __name__ == "__main__":
    sys.exit(main())

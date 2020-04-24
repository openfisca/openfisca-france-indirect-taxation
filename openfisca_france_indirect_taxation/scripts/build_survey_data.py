import argparse
import datetime
import logging
import os
import sys


from openfisca_france_indirect_taxation.build_survey_data.run_all import run


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def main():
    parser = argparse.ArgumentParser()
    all_years = [2011]
    parser.add_argument('-y', '--years', nargs='+', help = "years of survey to build (default = {})'".format(all_years), default = all_years)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    start_time = datetime.datetime.now()
    years_calage = [int(year) for year in args.years]
    run(years_calage)

    log.info("The program has been executed in {}".format(datetime.datetime.now() - start_time))

    return 0


if __name__ == "__main__":
    sys.exit(main())

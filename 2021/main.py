import copy
import datetime
from selenium.common.exceptions import NoSuchElementException

from Parser import GrandmasterParser
from GrandmasterPool import GrandmasterPool
from GrandmasterRankCollection import RankCollection
from DFPlotter import plot_dataframe_pretty
import tweet_api
import Util


def run(event, context):
    print(datetime.datetime.now())
    print('start run!')
    regions = ['NA', 'EU', 'APAC']
    path_prefix = '/tmp/' if Util.is_aws() else ''
    for region in regions:
        gm_pool = GrandmasterPool()
        parser = GrandmasterParser(gm_pool, path_prefix)
        num_runs = 100000
        original_parsed_league = None
        while original_parsed_league is None:
            try:
                original_parsed_league = parser.parse_league(region)
            except NoSuchElementException:
                pass
            if original_parsed_league is None:
                break
        print(datetime.datetime.now())
        print('parse is done')
        if original_parsed_league is None:
            print('nothing to do because this league is already parsed!')
        else:
            gmrc = RankCollection()
            for i in range(num_runs):
                parsed_league = copy.deepcopy(original_parsed_league)
                parsed_league.finish()
                rank = parsed_league.get_ranks()
                gmrc.add_result(rank)
            print(datetime.datetime.now())
            print('simulation done')

            gm_array = gmrc.export_to_array()
            plot_dataframe_pretty(gm_array, region + ' Grandmaster standings', num_runs, path_prefix + region + '.png')

            tweet_api.post_picture(path_prefix + region + '.png')
            print(datetime.datetime.now())
            print('tweet post done')

    return {
        'statusCode': 200,
        'body': None
    }


if __name__ == '__main__':
    run(None, None)

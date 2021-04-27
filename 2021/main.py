import json
import copy
import tweet_api
import datetime
from Parser import GrandmasterParser
from GrandmasterPool import GrandmasterPool
from GrandmasterRankCollection import RankCollection
from DFPlotter import plot_dataframe_pretty
from selenium.common.exceptions import NoSuchElementException


def run(event, context):
    print(datetime.datetime.now())
    print('start run!')
    regions = ['NA', 'EU', 'APAC']
    for region in regions:
        gm_pool = GrandmasterPool()
        parser = GrandmasterParser(gm_pool)
        num_runs = 100000
        original_parsed_league = None
        while original_parsed_league is None:
            try:
                original_parsed_league = parser.parse_league(region)
            except NoSuchElementException:
                pass
        print(datetime.datetime.now())
        print('parse is done')
        gmrc = RankCollection()
        for i in range(num_runs):
            parsed_league = copy.deepcopy(original_parsed_league)
            parsed_league.finish()
            rank = parsed_league.get_ranks()
            gmrc.add_result(rank)
        print(datetime.datetime.now())
        print('simulation done')

        data_frame = gmrc.export_to_df()
        plot_dataframe_pretty(data_frame, region + ' Grandmaster standings', num_runs, region + '.png')

        #tweet_api.post_picture(region + '.png')
        print(datetime.datetime.now())
        print('tweet post done')

    return {
        'statusCode': 200,
        'body': None
    }


if __name__ == '__main__':
    run(None, None)

import copy
import datetime
from selenium.common.exceptions import NoSuchElementException

from Parser import GrandmasterParser
from GrandmasterPool import GrandmasterPool
from GrandmasterRankCollection import RankCollection, RankCollectionForPlayoff
from DFPlotter import plot_dataframe_pretty
import tweet_api
import Util


def run(event, context):
    print(datetime.datetime.now())
    print('start run!')
    print(event)
    print(context)
    regions = ['NA', 'EU', 'APAC']
    path_prefix = '/tmp/' if Util.is_aws() else ''
    for region in regions:
        gm_pool = GrandmasterPool()
        parser = GrandmasterParser(gm_pool, Util.is_aws())
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
            rank_collection = RankCollection()
            rank_collection_for_playoff = RankCollectionForPlayoff()
            for i in range(num_runs):
                parsed_league = copy.deepcopy(original_parsed_league)
                parsed_league.finish()
                rank = parsed_league.get_ranks()
                rank_collection.add_result(rank)
                rank_collection_for_playoff.add_result(rank)
            print(datetime.datetime.now())
            print('simulation done')

            gm_array = rank_collection.export_to_array()
            print(gm_array)
            plot_dataframe_pretty(gm_array, region + ' Grandmaster standings',
                                  num_runs, path_prefix + region + '.png', False)
            gm_array_for_playoff = rank_collection_for_playoff.export_to_array()
            print(gm_array_for_playoff)
            plot_dataframe_pretty(gm_array_for_playoff, region + ' Grandmaster playoff',
                                  num_runs, path_prefix + region + '_playoff.png', True)

            datetime_parsed = datetime.datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%SZ')
            datetime_formatted = datetime.datetime.strftime(datetime_parsed, '%H:%M (UTC) on %b %d, %Y')
            tweet_api.post_picture_and_message(path_prefix + region + '.png',
                                               'Grandmaster standing as of ' + datetime_formatted)
            tweet_api.post_picture_and_message(path_prefix + region + '_playoff.png',
                                               'Grandmaster playoff odds as of ' + datetime_formatted)
            print(datetime.datetime.now())
            print('tweet post done')

    return {
        'statusCode': 200,
        'body': None
    }


if __name__ == '__main__':
    run({
        'version': '0',
        'id': '38228180-d144-c56d-e335-401ed607e83b',
        'detail-type': 'Scheduled Event',
        'source': 'aws.events',
        'account': '387228731976',
        'time': '2021-05-15T07:00:00Z',
        'region': 'us-east-2',
        'resources': ['arn:aws:events:us-east-2:387228731976:rule/5mins'],
        'detail': {}
    }, None)

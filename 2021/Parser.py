import json
import os
import typing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

from GrandmasterWeek import GrandmasterWeek, EmptyGrandmasterWeek, Tournament, DualTournament
from GrandmasterPool import GrandmasterPool
from GrandmasterLeague import GrandMasterLeague
from Grandmaster import GrandMaster
from Match import Match
import S3Client
import Util


def parse_bracket_match(competitors: typing.List[WebElement],
                        competitor_list: typing.List[GrandMaster], grandmaster_pool: GrandmasterPool) -> Match:
    winner = None
    loser = None
    participants = list()
    for competitor in competitors:
        competitor_name = competitor.find_element_by_class_name('BracketMatchCompetitor-name').text

        competitor_from_pool = None
        if competitor_name != '-' and 'Loser of' not in competitor_name and 'Winner of' not in competitor_name:
            competitor_from_pool = grandmaster_pool.get_master_by_name(competitor_name)

        if competitor_from_pool is not None and \
                competitor_from_pool.name not in [competitor.name for competitor in competitor_list]:
            competitor_list.append(competitor_from_pool)

        competitor_class = competitor.get_attribute('class')
        participants.append(competitor_from_pool)
        if 'matchWin' in competitor_class:
            winner = competitor_from_pool
        elif 'matchLoss' in competitor_class:
            loser = competitor_from_pool
    # hard coding for 15-people NA league
    if winner is not None and loser is None:
        participants.append(grandmaster_pool.get_master_by_name('-'))
    is_first_player_won = None
    if winner is not None:
        is_first_player_won = (participants[0].name == winner.name)
    if not participants:
        participants = [None, None]
    match = Match(participants, is_first_player_won)
    return match


def get_driver():
    is_aws = Util.is_aws()
    if is_aws:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x768')
        chrome_options.add_argument('--user-data-dir=/tmp/user-data')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path=/tmp/data-path')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir=/tmp')
        chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/61.0.3163.100 Safari/537.36')
        chrome_options.binary_location = "/opt/python/bin/headless-chromium"

        driver = webdriver.Chrome('/opt/python/bin/chromedriver', chrome_options=chrome_options)
        return driver
    else:
        from chromedriver_py import binary_path
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x768')
        driver = webdriver.Chrome(executable_path=binary_path, chrome_options=chrome_options)
        return driver


class GrandmasterParser:
    def __init__(self, pool, is_aws):
        self.driver = get_driver()
        self.pool = pool
        self.is_aws = is_aws
        self.turn_new_week = False

    def parse(self, url):
        if self.turn_new_week:
            return EmptyGrandmasterWeek(self.pool.get_masters())
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        dual_tournament = self.driver.find_element_by_class_name('DualTournament')
        dual_tournament_groups = dual_tournament.find_elements_by_class_name('DualTournamentGroup')
        parsed_dual_tournaments = list()
        for dual_tournament_group in dual_tournament_groups:
            competitor_list = list()
            initials = [None, None]
            winners = None
            losers = None
            decider = None
            dual_tournament_group_button = dual_tournament_group.find_element_by_class_name('DualTournamentGroupButton')
            dual_tournament_group_button.click()
            bracket_matches = self.driver.find_elements_by_class_name('BracketMatch')
            for bracket_match in bracket_matches:
                competitors = bracket_match.find_elements_by_class_name('BracketMatchCompetitor')
                match = parse_bracket_match(competitors, competitor_list, self.pool)
                match_id = bracket_match.find_element_by_class_name('BracketMatch-id').text
                if match_id == 'U1':
                    initials[0] = match
                elif match_id == 'U2':
                    initials[1] = match
                elif match_id == 'U3':
                    winners = match
                elif match_id == 'E1':
                    losers = match
                elif match_id == 'E2':
                    decider = match

            # hard coding for 15-people NA league
            if len(competitor_list) == 3:
                competitor_list.append(self.pool.get_master_by_name('-'))

            parsed_dual_tournament = None
            if len(competitor_list) == 4:
                parsed_dual_tournament = DualTournament(competitor_list, (initials, winners, losers, decider))
            parsed_dual_tournaments.append(parsed_dual_tournament)

            bracket_heading_button = self.driver.find_element_by_class_name('BracketHeadingButton')
            bracket_heading_button.click()
        top_8_button = self.driver.find_elements_by_class_name('StageBtn')[1]
        top_8_button.click()
        single_elimination_matches = self.driver.find_elements_by_class_name('BracketMatch')
        competitor_list = list()
        quarterfinals = list()
        semifinals = list()
        finals = None
        for bracket_match in single_elimination_matches:
            competitors = bracket_match.find_elements_by_class_name('BracketMatchCompetitor')
            match = parse_bracket_match(competitors, competitor_list, self.pool)
            match_id = bracket_match.find_element_by_class_name('BracketMatch-id').text
            match_id_num = int(match_id[1])
            if match_id_num <= 4:
                quarterfinals.append(match)
            elif 4 < match_id_num <= 6:
                semifinals.append(match)
            else:
                finals = match
        parsed_tournament = None
        if quarterfinals != [None, None, None, None]:
            parsed_tournament = Tournament(competitor_list, (quarterfinals, semifinals, finals))
        if parsed_dual_tournaments == [None, None, None, None]:
            parsed_week = EmptyGrandmasterWeek(self.pool.get_masters())
            self.turn_new_week = True
        else:
            parsed_week = GrandmasterWeek(parsed_dual_tournaments, parsed_tournament)
        parsed_week.validate()
        return parsed_week

    def parse_league(self, locale):
        cached_league = None
        cached_league_json = None
        if self.is_aws:
            raw_cached = S3Client.from_file(locale + '.json')
            if raw_cached is not None:
                cached_league_json = json.loads(raw_cached)
                cached_league = GrandMasterLeague.init_from_json(cached_league_json, self.pool)
        else:
            if os.path.isfile(locale + '.json'):
                with open(locale + '.json', 'r') as cached_file:
                    cached_league_json = json.load(cached_file)
                    cached_league = GrandMasterLeague.init_from_json(cached_league_json, self.pool)
        if cached_league_json is not None:
            print('found cached file:')
            print(cached_league_json)
        grandmaster_weeks = cached_league.weeks if cached_league is not None else [None] * 7
        for week in range(7):
            if grandmaster_weeks[week] is not None and grandmaster_weeks[week].tournament is not None\
                    and grandmaster_weeks[week].tournament.final is not None:
                continue

            grandmaster_url =\
                'https://playhearthstone.com/en-us/esports/standings/?region=%s&seasonId=2&stage=%i&year=2021'\
                % (locale, week)
            grandmaster_week = self.parse(grandmaster_url)
            grandmaster_weeks[week] = grandmaster_week
        parsed_league = GrandMasterLeague(self.pool.get_masters(), grandmaster_weeks)
        parsed_league_json = parsed_league.export()
        if cached_league_json == parsed_league_json:
            # Nothing changed since last run
            return None
        if self.is_aws:
            raw_parsed = json.dumps(parsed_league_json)
            S3Client.to_file(raw_parsed, locale + '.json')
        else:
            with open(locale + '.json', 'w') as league_json:
                json.dump(parsed_league_json, league_json)
        return parsed_league


if __name__ == '__main__':
    gm_pool = GrandmasterPool()
    parser = GrandmasterParser(gm_pool, False)
    # parser.parse('https://playhearthstone.com/en-us/esports/standings/?region=NA&seasonId=1&stage=0&year=2021')
    original_parsed_league = parser.parse_league('NA')

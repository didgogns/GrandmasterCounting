import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from GrandmasterWeek import GrandmasterWeek, EmptyGrandmasterWeek, Tournament, DualTournament
from GrandmasterPool import GrandmasterPool
from GrandmasterLeague import GrandMasterLeague
import Util


def parse_bracket_match(competitors, competitor_list, grandmaster_pool, is_top_8):
    match = [None, None]
    for competitor in competitors:
        competitor_name = competitor.find_element_by_class_name('BracketMatchCompetitor-name').text

        if not is_top_8:
            # hard coding for 15-people NA league
            if competitor_name is not '-' and\
                    'Loser of' not in competitor_name and 'Winner of' not in competitor_name:
                competitor_list.add(competitor_name)
            if 'Loser of' in competitor_name:
                competitor_name = '-'
        elif competitor_name is not '-' and\
                competitor_name not in competitor_list and 'Winner of' not in competitor_name:
            competitor_list.append(competitor_name)

        competitor_class = competitor.get_attribute('class')
        if 'matchWin' in competitor_class:
            match[0] = grandmaster_pool.get_master_by_name(competitor_name)
        elif 'matchLoss' in competitor_class:
            match[1] = grandmaster_pool.get_master_by_name(competitor_name)
    if match[0] is None:
        match = None
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
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
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
    def __init__(self, pool, path_prefix):
        self.driver = get_driver()
        self.pool = pool
        self.path_prefix = path_prefix
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
            competitor_list = set()
            initials = [None, None]
            winners = None
            losers = None
            decider = None
            dual_tournament_group_button = dual_tournament_group.find_element_by_class_name('DualTournamentGroupButton')
            dual_tournament_group_button.click()
            bracket_matches = self.driver.find_elements_by_class_name('BracketMatch')
            for bracket_match in bracket_matches:
                competitors = bracket_match.find_elements_by_class_name('BracketMatchCompetitor')
                match = parse_bracket_match(competitors, competitor_list, self.pool, False)
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
                competitor_list.add('-')

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
            match = parse_bracket_match(competitors, competitor_list, self.pool, True)
            match_id = bracket_match.find_element_by_class_name('BracketMatch-id').text
            match_id_num = int(match_id[1])
            if match_id_num <= 4:
                quarterfinals.append(match)
            elif 4 < match_id_num <= 6:
                semifinals.append(match)
            else:
                finals = match
        parsed_tournament = None
        if quarterfinals is not [None, None, None, None]:
            parsed_tournament = Tournament([self.pool.get_master_by_name(competitor) for competitor in competitor_list],
                                           (quarterfinals, semifinals, finals))
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
        if os.path.isfile(self.path_prefix + locale + '.json'):
            with open(self.path_prefix + locale + '.json', 'r') as cached_file:
                cached_league_json = json.load(cached_file)
                cached_league = GrandMasterLeague.from_dict(cached_league_json, self.pool)
        grandmaster_weeks = cached_league.weeks if cached_league is not None else [None] * 7
        for week in range(7):
            if grandmaster_weeks[week] is not None and grandmaster_weeks[week].tournament is not None\
                    and grandmaster_weeks[week].tournament.final is not None:
                continue

            # TODO change seasonId later
            grandmaster_url =\
                'https://playhearthstone.com/en-us/esports/standings/?region=%s&seasonId=1&stage=%i&year=2021'\
                % (locale, week)
            grandmaster_week = self.parse(grandmaster_url)
            grandmaster_weeks[week] = grandmaster_week
        parsed_league = GrandMasterLeague(self.pool.get_masters(), grandmaster_weeks)
        parsed_league_json = GrandMasterLeague.to_dict(parsed_league)
        if cached_league_json == parsed_league_json:
            # Nothing changed since last run
            return None
        with open(self.path_prefix + locale + '.json', 'w') as league_json:
            json.dump(parsed_league_json, league_json)
        return parsed_league


if __name__ == '__main__':
    gm_pool = GrandmasterPool()
    parser = GrandmasterParser(gm_pool)
    # parser.parse('https://playhearthstone.com/en-us/esports/standings/?region=NA&seasonId=1&stage=0&year=2021')
    original_parsed_league = parser.parse_league('NA')

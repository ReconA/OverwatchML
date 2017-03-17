import requests
import json

# REGIONS
AMERICAS = 'us'
EUROPE = 'eu'
KOREA = 'kr'

# PLATFORMS
PC = 'pc'

# MODES
COMP = 'competitive'
QUICK = 'quickplay'

hero_list = {
    'ANA': 'Ana',
    'BASTION': 'Bastion',
    'DIVA': 'DVa',
    'GENJI': 'Genji',
    'HANZO': 'Hanzo',
    'JUNKRAT': 'Junkrat',
    'LUCIO': 'Lucio',
    'MCCREE': 'McCree',
    'MEI': 'Mei',
    'MERCY': 'Mercy',
    'PHARAH': 'Pharah',
    'REAPER': 'Reaper',
    'REINHARDT': 'Reinhardt',
    'ROADHOG': 'Roadhog',
    'SOLDIER_76': 'Soldier76',
    'SOMBRA': "Sombra",
    'SYMMETRA': 'Symmetra',
    'TORBJOERN': 'Torbjoern',
    'TRACER': 'Tracer',
    'WIDOWMAKER': 'Widowmaker',
    'WINSTON': 'Winston',
    'ZARYA': 'Zarya',
    'ZENYATTA': 'Zenyatta'
}


class OverwatchApi:

    def get_platforms(self, battle_tag):
        return self._base_request(
            battle_tag,
            'get-platforms'
        )

    def get_profile(self, battle_tag):
        battle_tag = self.sanitize_battletag(battle_tag)
        r = requests.get(
                'http://localhost:9000/{platform}/{region}/{battle_tag}/profile'.format(
                platform="pc",
                region="us",
                battle_tag=battle_tag,
                mode="competitive",
            )
         )

        self.validate_response(r)
        return r.json()

    def get_stats_all_heroes(self, battle_tag):
        return self._base_request(
            battle_tag,
            'allHeroes/'
        )

    def get_stats_selected_heroes(self, battle_tag, _heroes):
        # url encode for comma
        _heroes = '%2C'.join(_heroes)
        return self._base_request(
            battle_tag,
            'hero/' + _heroes + '/'
        )

    def get_hero_stats(self, battle_tag, hero):
        return self._base_request(
            battle_tag,
            'hero/' + hero + '/'
        )

    def get_stats_heroes_used(self, battle_tag):
        return self._base_request(
            battle_tag,
            'heroes'
        )

    def get_every_hero_stat(self, battle_tag):
        return self.get_stats_selected_heroes(battle_tag, hero_list.values())

    def validate_response(self, response):
        if response.status_code != 200:
            print "Resp=%s code is not 200" %response
            raise Exception

    def sanitize_battletag(self, battle_tag):
        if '#' in battle_tag:
            battle_tag = battle_tag.replace('#', '-')
        return battle_tag

    def _base_request(self, battle_tag, url):
        battle_tag = self.sanitize_battletag(battle_tag)
        req = 'http://localhost:9000/{platform}/{region}/{battle_tag}/{mode}/{url}'.format(
                platform="pc",
                region="us",
                battle_tag=battle_tag,
                #mode="competitive",
                mode="competitive",
                url=url)
        #print req
        r = requests.get(req)
        self.validate_response(r)
        return r.json()

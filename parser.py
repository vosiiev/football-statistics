import requests
from bs4 import BeautifulSoup
from bs4 import element
from operator import itemgetter
import argparse



LEAGUES = [
    'premier-league',
    'championship',
    'league-one',
    'league-two',
    'conference',
    'scottish-premiership',
    'scottish-championship',
    'la-liga',
    'segunda',
    'bundesliga-1',
    'bundesliga-2',
    'serie-a',
    'serie-b',
    'ligue-1',
    'primeira-liga',
    'eredivisie',
    'jupiler-league',
]


'''
standart, form, home, away, half, goals, bts, over15,
over25, over35, booking, corner, sbh, clean, avggoals,
avggoalsht, avgodds, referees
'''
def get_table(table_type='corner', league='premier-league'):
    page = requests.get(f'https://www.cheekypunter.com/stats/{league}/#data-import-corner')
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('div', id=f'tabs-{table_type}-2019')
    rows = table.find_all('tr')
    headers = table.find_all('th')
    headers = [item.text.strip() for item in headers]

    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [item.text.strip() for item in cols]
        values = [item for item in cols if item]

        tmp = {}
        for i in range(len(headers)):
            try:
                tmp[headers[i]] = float(values[i])
            except IndexError:
                pass
            except ValueError:
                tmp[headers[i]] = values[i]

        data.append(tmp)

    return data[1:]

def percent_to_float(x):
    return round(float(x.strip('%'))/100, 2)

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type',
                        type=str,
                        help='''Choose type among: standart, form, home,
                        away, half, goals, bts, over15, over25, over35,
                        booking, corner, sbh, clean, avggoals,
                        avggoalsht, avgodds, referees'''
                        )
    parser.add_argument('-l', '--league',
                        type=str,
                        help='''Choose league among: premier-league, championship,
                            league-one, league-two, conference,
                            scottish-premiership, scottish-championship,
                            la-liga, segunda, bundesliga-1, bundesliga-2,
                            serie-a, serie-b, ligue-1, primeira-liga,
                            eredivisie, jupiler-league'''
                        )
    args = parser.parse_args()
    return args.type, args.league

def main():
    table_type, league = cli()
    data = None
    if table_type and league:
        data = get_table(table_type=table_type, league=league)
    elif table_type:
        data = get_table(table_type=table_type)
    elif league:
        data = get_table(league=league)

    else:
        data = get_table()

    for team in data:
        for key in team.keys():
            if '%' in key:
                team[key] = percent_to_float(team[key])

    data = sorted(data, key=itemgetter('Team'))

    for item in data:
        print(item)

if __name__ == '__main__':
    main()


# with open('today.txt', 'r') as f:
#     for line in f:
#         rf = line.split()
#         for item in data:
#             if rf[0] in item.values() or rf[1] in item.values():
#                 print(item)

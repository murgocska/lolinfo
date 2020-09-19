import requests
from django.shortcuts import render


def home(request):
    summonername = request.GET.get('nickname')
    return render(request, 'data/home.html')


def data(request):
    region = 'eun1'
    APIKey = 'RGAPI-1e6d6008-48cc-411e-88cf-f74a2074fb79'
    summonername = request.GET.get('nickname')


    url = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonername + '?api_key=' + APIKey
    r = requests.get(url).json()
    if '"status_code":404' in r:
        data = {
            'error': 'Nincs ilyen felhasználó'
        }
    else:
        summonerid = r['id']
        accountid = r['accountId']
        #matchid = ''
        profileicon = str(r['profileIconId'])

        url2 = 'https://' + region + '.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summonerid + '?api_key=' + APIKey
        r = requests.get(url2).json()

        winrate = (r[0]['wins'] / (r[0]['wins'] + r[0]['losses'])) * 100
        winrate = float("{:.2f}".format(winrate))
        print(url2)

        data = {
            'nickname': r[0]['summonerName'],
            'tier': r[0]['tier'],
            'rank': r[0]['rank'],
            'lp': r[0]['leaguePoints'],
            'wins': r[0]['wins'],
            'losses': r[0]['losses'],
            'winrate': winrate,
            'profileicon': 'data/' + profileicon,

        }
    context = {'data': data}
    return render(request, 'data/data.html', context)
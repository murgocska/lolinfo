import requests
from django.shortcuts import render


def home(request):
    summonername = request.GET.get('nickname')
    region = request.GET.get('region')
    return render(request, 'data/home.html')


def data(request):
    #region = 'eun1'
    APIKey = 'RGAPI-730cc9dd-27da-4941-a291-074fbc3d6f97'
    summonername = request.GET.get('nickname')
    region = request.GET.get('region')

    url = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonername + '?api_key=' + APIKey
    print(url)
    r = requests.get(url).json()
    summonerid = r['id']
    accountid = r['accountId']
    #matchid = ''
    profileicon = str(r['profileIconId'])

    url = 'https://' + region + '.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summonerid + '?api_key=' + APIKey
    r = requests.get(url).json()


    basicinfo = {
        'nickname': r[0]['summonerName'],
        'profileicon': 'data/' + profileicon,
    }
    rankicon=r[0]['tier']
    rankicon = str(r[0]['tier'])
    solo = {
        'tier': r[0]['tier'],
        'rank': r[0]['rank'],
        'lp': r[0]['leaguePoints'],
        'wins': r[0]['wins'],
        'losses': r[0]['losses'],
        'rankicon': 'data/' + rankicon,
    }
    rankicon=r[1]['tier']
    flex = {
        'tier': r[1]['tier'],
        'rank': r[1]['rank'],
        'lp': r[1]['leaguePoints'],
        'wins': r[1]['wins'],
        'losses': r[1]['losses'],
        'rankicon': 'data/' + rankicon,
    }

    winrate = (solo['wins'] / (solo['wins'] + solo['losses'])) * 100
    winrate=float("{:.2f}".format(winrate))
    solo['winrate'] = winrate
    winrate = (flex['wins'] / (flex['wins'] + flex['losses'])) * 100
    winrate=float("{:.2f}".format(winrate))
    flex['winrate'] = winrate

    context = {
        'basicinfo': basicinfo,
        'solo': solo,
        'flex': flex,
    }
    return render(request, 'data/data.html', context)
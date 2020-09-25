import requests
from django.shortcuts import render


def home(request):
    summonername=request.GET.get('nickname')
    region=request.GET.get('region')
    return render(request, 'data/home.html')


def data(request):
    APIKey='RGAPI-cdef08bd-0793-4029-828a-d3bee5855518'
    summonername=request.GET.get('nickname')
    region=request.GET.get('region')

    url='https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonername + '?api_key=' + APIKey
    print(url)
    r=requests.get(url).json()

    try:
        summonerid=r['id']
    except:
        return render(request, 'data/nosumms.html')
    else:
        # accountid = r['accountId']
        # matchid = ''
        profileicon=str(r['profileIconId'])

        url='https://' + region + '.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summonerid + '?api_key=' + APIKey
        r=requests.get(url).json()
        print(url)
        queuelen=len(r)

        rankicon='placeholder'
        solo={
            'tier': 'UNRANKED',
            'rank': 'UNRANKED',
            'lp': 'UNRANKED',
            'wins': 'UNRANKED',
            'losses': 'UNRANKED',
            'rankicon': 'data/' + rankicon,
        }
        flex={
            'tier': 'UNRANKED',
            'rank': 'UNRANKED',
            'lp': 'UNRANKED',
            'wins': 'UNRANKED',
            'losses': 'UNRANKED',
            'rankicon': 'data/' + rankicon,
        }

        if queuelen == 0:
            basicinfo={
                'nickname': request.GET.get('nickname'),
                'profileicon': 'data/' + profileicon,
            }
        else:
            basicinfo={
                'nickname': r[0]['summonerName'],
                'profileicon': 'data/' + profileicon,
            }
        # print(r[0]['queueType'])
        if queuelen == 2:
            if r[0]['queueType'] == 'RANKED_SOLO_5x5':
                print('1. if')
                rankicon=str(r[0]['tier'])
                solo.clear()
                solo={
                    'tier': r[0]['tier'],
                    'rank': r[0]['rank'],
                    'lp': r[0]['leaguePoints'],
                    'wins': r[0]['wins'],
                    'losses': r[0]['losses'],
                    'rankicon': 'data/' + rankicon,
                }
            elif r[1]['queueType'] == 'RANKED_SOLO_5x5':
                print('2. if')
                rankicon=str(r[1]['tier'])
                solo.clear()
                solo={
                    'tier': r[1]['tier'],
                    'rank': r[1]['rank'],
                    'lp': r[1]['leaguePoints'],
                    'wins': r[1]['wins'],
                    'losses': r[1]['losses'],
                    'rankicon': 'data/' + rankicon,
                }
            else:
                print('ELSE')
        elif queuelen == 1:
            if r[0]['queueType'] == 'RANKED_SOLO_5x5':
                print('1. if')
                rankicon=str(r[0]['tier'])
                solo.clear()
                solo={
                    'tier': r[0]['tier'],
                    'rank': r[0]['rank'],
                    'lp': r[0]['leaguePoints'],
                    'wins': r[0]['wins'],
                    'losses': r[0]['losses'],
                    'rankicon': 'data/' + rankicon,
                }
        else:
            print('ELSESOLO')
        if queuelen == 2:
            if r[0]['queueType'] == 'RANKED_FLEX_SR':
                rankicon=str(r[0]['tier'])
                flex.clear()
                flex={
                    'tier': r[0]['tier'],
                    'rank': r[0]['rank'],
                    'lp': r[0]['leaguePoints'],
                    'wins': r[0]['wins'],
                    'losses': r[0]['losses'],
                    'rankicon': 'data/' + rankicon,
                }
            elif r[1]['queueType'] == 'RANKED_FLEX_SR':
                rankicon=str(r[1]['tier'])
                flex.clear()
                flex={
                    'tier': r[1]['tier'],
                    'rank': r[1]['rank'],
                    'lp': r[1]['leaguePoints'],
                    'wins': r[1]['wins'],
                    'losses': r[1]['losses'],
                    'rankicon': 'data/' + rankicon,
                }
            else:
                print('ELSEflex')
        elif queuelen == 1:
            if r[0]['queueType'] == 'RANKED_FLEX_SR':
                print('1. if')
                rankicon=str(r[0]['tier'])
                solo.clear()
                solo={
                    'tier': r[0]['tier'],
                    'rank': r[0]['rank'],
                    'lp': r[0]['leaguePoints'],
                    'wins': r[0]['wins'],
                    'losses': r[0]['losses'],
                    'rankicon': 'data/' + rankicon,
                }
        else:
            print('ELSEFLEX')

        if solo['wins'] != 'UNRANKED':
            winrate=(solo['wins'] / (solo['wins'] + solo['losses'])) * 100
            winrate=float("{:.2f}".format(winrate))
            solo['winrate']=winrate
        else:
            solo['winrate']=0
        if flex['wins'] != 'UNRANKED':
            winrate=(flex['wins'] / (flex['wins'] + flex['losses'])) * 100
            winrate=float("{:.2f}".format(winrate))
            flex['winrate']=winrate
        else:
            flex['winrate']=0


        context={
            'basicinfo': basicinfo,
            'solo': solo,
            'flex': flex,
        }
    return render(request, 'data/data.html', context)

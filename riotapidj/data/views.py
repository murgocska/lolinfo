import datetime
import requests
import json
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
        accountid=r['accountId']
        profileicon='profileicons/' + str(r['profileIconId'])

        url='https://' + region + '.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summonerid + '?api_key=' + APIKey
        r=requests.get(url).json()
        print(url)
        queuelen=len(r)

        rankicon='placeholder'
        solo={
            'tier': 'UNRANKED',
            'rank': '',
            'lp': 0,
            'wins': 'UNRANKED',
            'losses': 'UNRANKED',
            'rankicon': 'data/rankicons/' + rankicon,
        }
        flex={
            'tier': 'UNRANKED',
            'rank': '',
            'lp': 0,
            'wins': 'UNRANKED',
            'losses': 'UNRANKED',
            'rankicon': 'data/rankicons/' + rankicon,
        }

        if queuelen == 0:
            basicinfo={
                'nickname': request.GET.get('nickname'),
                'profileicon': 'data/' + profileicon,
                'region': region
            }
        else:
            basicinfo={
                'nickname': r[0]['summonerName'],
                'profileicon': 'data/' + profileicon,
                'region': region
            }
        # print(r[0]['queueType'])
        if queuelen == 2:
            if r[0]['queueType'] == 'RANKED_SOLO_5x5':
                rankicon=str(r[0]['tier'])
                solo.clear()
                solo={
                    'tier': r[0]['tier'],
                    'rank': r[0]['rank'],
                    'lp': r[0]['leaguePoints'],
                    'wins': r[0]['wins'],
                    'losses': r[0]['losses'],
                    'rankicon': 'data/rankicons/' + rankicon,
                }
            elif r[1]['queueType'] == 'RANKED_SOLO_5x5':
                rankicon=str(r[1]['tier'])
                solo.clear()
                solo={
                    'tier': r[1]['tier'],
                    'rank': r[1]['rank'],
                    'lp': r[1]['leaguePoints'],
                    'wins': r[1]['wins'],
                    'losses': r[1]['losses'],
                    'rankicon': 'data/rankicons/' + rankicon,
                }
            else:
                print('ELSE')
        elif queuelen == 1:
            if r[0]['queueType'] == 'RANKED_SOLO_5x5':
                rankicon=str(r[0]['tier'])
                solo.clear()
                solo={
                    'tier': r[0]['tier'],
                    'rank': r[0]['rank'],
                    'lp': r[0]['leaguePoints'],
                    'wins': r[0]['wins'],
                    'losses': r[0]['losses'],
                    'rankicon': 'data/rankicons/' + rankicon,
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
                    'rankicon': 'data/rankicons/' + rankicon,
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
                    'rankicon': 'data/rankicons/' + rankicon,
                }
            else:
                print('ELSEflex')
        elif queuelen == 1:
            if r[0]['queueType'] == 'RANKED_FLEX_SR':
                rankicon=str(r[0]['tier'])
                solo.clear()
                solo={
                    'tier': r[0]['tier'],
                    'rank': r[0]['rank'],
                    'lp': r[0]['leaguePoints'],
                    'wins': r[0]['wins'],
                    'losses': r[0]['losses'],
                    'rankicon': 'data/rankicons/' + rankicon,
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

        url='https://' + region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountid + '?api_key=' + APIKey
        r=requests.get(url).json()
        matches=[]
        for x in range(10):
            matches.append([r['matches'][x]['gameId']])
            x+=1
        lastmatch=str(matches[0])
        lastmatch=lastmatch[1:-1]

        url='https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + lastmatch + '?api_key=' + APIKey
        r=requests.get(url).json()
        print(url)

        f=open('championFull.json', "r")
        allchamp=json.loads(f.read())
        lastmatch={}
        x=0
        for x in range(10):
            playerid=r['participants'][x]['participantId']
            playername=r['participantIdentities'][x]['player']['summonerName']
            champid=r['participants'][playerid - 1]['championId']

            champ=allchamp['keys'][str(champid)]
            champname=allchamp['data'][champ]['name']
            champicon=allchamp['data'][champ]['image']['full']

            lastmatch['player' + str(x) + 'name']=playername
            lastmatch['player' + str(x) + 'champicon']='data/champions/' + champicon

        context={
            'basicinfo': basicinfo,
            'solo': solo,
            'flex': flex,
            'lastmatch': lastmatch
        }
    return render(request, 'data/data.html', context)


def champions(request):
    return render(request, 'data/champions.html')


def live_game(request):
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
        url='https://' + region + '.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/' + summonerid + '?api_key=' + APIKey
        print(url)
        r=requests.get(url).json()

        f=open('queues.json', "r")
        data=json.loads(f.read())

        gameinfo = {}
        queuetype=r['gameQueueConfigId']
        x=0
        while True:
            adat=data[x]['queueId']
            if adat == queuetype:
                print('Játszott pálya: ' + data[x]['map'] + data[x]['description'])
                gameinfo['gamemap'] = data[x]['map']
                gameinfo['gamemode'] = data[x]['description']
                break
            x+=1

        gamestarttime = r['gameStartTime']
        date = gamestarttime / 1000
        date = datetime.datetime.fromtimestamp(date)
        date.strftime('%Y-%m-%d %H:%M:%S')
        print(date)
        gameinfo['gamestarttime'] = date.strftime('%Y-%m-%d %H:%M:%S')


        #gameinfo['gamestarttime'] = r['gameStartTime']


        f=open('championFull.json', "r")
        allchamp=json.loads(f.read())
        lastmatch={}
        x=0
        for x in range(10):
            playername=r['participants'][x]['summonerName']
            champid=r['participants'][x]['championId']

            champ=allchamp['keys'][str(champid)]
            champname=allchamp['data'][champ]['name']
            champicon=allchamp['data'][champ]['image']['full']

            lastmatch['player' + str(x) + 'name']=playername
            lastmatch['player' + str(x) + 'champicon']='data/champions/' + champicon


        basicinfo={
            'region': region,
            'summonername': summonername,
        }

    context={
        'basicinfo': basicinfo,
        'lastmatch': lastmatch,
        'gameinfo': gameinfo,
    }
    return render(request, 'data/live_game.html', context)

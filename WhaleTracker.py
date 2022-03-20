import requests
import json
import time
import discord
client = discord.Client()

lastTxHash = open('lastTxHash.txt').read().strip()

def scanStats():
    headers = {
    'Host': 'api-juno.cosmostation.io',
    'Accept': 'application/json, text/plain, */*',
    }
    a = requests.get('https://api-juno.cosmostation.io/v1/account/new_txs/juno1aeh8gqu9wr4u8ev6edlgfq03rcy6v5twfn0ja8?limit=50&from=0',headers=headers,timeout=10)
    if a.status_code != 200:
        scanStats()
        return
    return json.loads(a.text)

@client.event
async def on_ready():
  global lastTxHash
  print(f'You have logged in as {client}')
  while(True):
    try:
        transactions = scanStats()
        if transactions[0]['data']['txhash'] == lastTxHash:
            time.sleep(60)
            continue
        else:
            newTxHash = transactions[0]['data']['txhash']
            for i in range(50):
                if transactions[i]['data']['txhash'] == lastTxHash:
                    break
                else:
                    if transactions[i]['data']['tx']['body']['messages'][0]['@type'] == '/cosmos.bank.v1beta1.MsgSend' and transactions[i]['data']['tx']['body']['messages'][0]['to_address'] != 'juno1aeh8gqu9wr4u8ev6edlgfq03rcy6v5twfn0ja8':
                        message = '**```juno1aeh8gqu9wr4u8ev6edlgfq03rcy6v5twfn0ja8 has sent '+str(round(float(transactions[i]['data']['tx']['body']['messages'][0]['amount'][0]['amount'])/1000000.0,2))+' Juno to '+transactions[i]['data']['tx']['body']['messages'][0]['to_address']+' at '+transactions[i]['data']['timestamp']+'```**'
                        messageSent = await client.get_channel(channelID).send(message)
                    elif transactions[i]['data']['tx']['body']['messages'][0]['@type'] == '/ibc.applications.transfer.v1.MsgTransfer':
                        message = '**```juno1aeh8gqu9wr4u8ev6edlgfq03rcy6v5twfn0ja8 has IBC transferred '+str(round(float(transactions[i]['data']['tx']['body']['messages'][0]['token']['amount'])/1000000,2))+' Juno at '+transactions[i]['data']['timestamp']+'```**'
                        messageSent = await client.get_channel(channelID).send(message)
                    elif transactions[i]['data']['tx']['body']['messages'][0]['@type'] == '/cosmos.staking.v1beta1.MsgUndelegate':
                        message = '**```juno1aeh8gqu9wr4u8ev6edlgfq03rcy6v5twfn0ja8 has undelegated '+str(round(float(transactions[i]['data']['tx']['body']['messages'][0]['amount']['amount'])/1000000.0,2))+' Juno at '+transactions[i]['data']['timestamp']+'```**'
                        messageSent = await client.get_channel(channelID).send(message)
            with open('lastTxHash.txt','w+') as j:
                j.write(newTxHash)
            lastTxHash = newTxHash
            time.sleep(60)
    except:
      continue

channelID = 0
BOT_TOKEN = 'PLACE_AUTH_TOKEN_HERE'
client.run(BOT_TOKEN)        
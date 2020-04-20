#EVERecruitmentFilter Developed by Karulean Valkyrie
#Version: 0.1 ALPHA



#---------------------[IMPORTDATA]

import sys
import string
import requests
import json
import cmd
import time
from joblib import Parallel, delayed
import multiprocessing
#---------------------[DATA]
NPCcorporation = ["1000165", "1000166", "1000077", "1000044", "1000045", "1000167", "1000169", "1000168", "1000115", "1000172", "1000170", "1000171", "1000066", "1000080", "1000072", "1000014", "1000009", "1000006", "1000107", "1000111", "1000114", "1000049", "1000046", "1000060"]
eveesicharsearch = "https://esi.evetech.net/latest/search/?categories=character&datasource=tranquility&language=en-us"

Charfile = open("CharacterData.txt", "r")
CharID = open("CharacterID.json", "w+")
#---------------------[CONSOLE CMDS]
CMDS = ["run", "help", "listcharamount", "convertchartoid", "filtertonpc", "exit"]


#---------------------[Library]
#convertdatatoids
def converttoids():
		ListChar = 0
		Charfile = open("CharacterData.txt", "r")
		with Charfile as CData:
			for nlines in CData:
				ListChar += 1
		print("There is", ListChar, "character loaded in dataset.")
		print("\nPlease wait.... Loading" , ListChar, "IDS to CharacterID.json")
		progress = -1
		maxdata = progress + 1
		readdata = open("CharacterData.txt", "r")
		CharID = open("CharacterID.json", "w+")
		CharID.writelines("["+"\n")
		for cids in readdata:
			maxdata += 1
			progress += 1
			prams = {"search": cids}
			req1 = requests.get(eveesicharsearch, params = prams)
			data = req1.json()
			ids = data["character"][0]
			#index ids to files
			if progress == ListChar - 1:
				CharID.writelines("\t"+str(ids)+"\n")
				print("\n", ids, cids, "\n Character Sorted", maxdata, "Out of", ListChar)
				CharID.writelines("]"+"\n")
				CharID.close()
				print("Complete...")
				time.sleep(1)
				break

			CharID.writelines("\t"+str(ids)+","+"\n") #so jank
			print("\n", ids, cids, "Character Sorted", maxdata, "Out of", ListChar)
			
		
			
#Testing
def postdiscordcmd():
	headers = {'Content-Type': 'application/json', 'Authorization': 'MjYwOTk0MDc4NTAwNTg1NDgz.Dw8_oQ.aclNOudoP1ubywRRRkiGrnUgMNA'}
	cidsl = input()
	pload = {'content': input()}
	pr = requests.post("https://discordapp.com/api/v6/channels/{}/messages".format(cidsl), data=pload, headers=headers)
	print(pr)

#bulkuploadidstoesi
def filteresicorp():
	#BULK publicDATA request
	headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
	payload = open("CharacterID.json", "rb")
	payloadinjector = requests.post("https://esi.evetech.net/latest/characters/affiliation/?datasource=tranquility&post_characters_affiliation_characters", data=payload, headers=headers)
	kdata = json.dumps(payloadinjector.json(), indent=1)	
	print(payloadinjector)
	print(kdata)

#manualsorting-slowmethod-greateraccuracies-blacklist
def manualsort():
	#checkamountofvalueindataset
	numPilot = 0
	CFile = open("CharacterData.txt", "r")
	with CFile as newData:
		for enlist in newData:
			numPilot +=1
	print("\n\nNumber of Names Detected:", numPilot)
	print("Filtering dataset to known NPC Corporation. Please wait....")
	
	
	#passvaluetoESIforid
	blacklist = open("Blacklist.txt", "a")
	rdata = open("CharacterData.txt", "r")
	results = open("results.txt", "w+")
	numPlist = 0
	newlineappend = 0
	
	for xcharacter in rdata:
		numPlist += 1
		fetchData = requests.get(eveesicharsearch, params = {"search": xcharacter})
		getData = fetchData.json()
		
		#check if char exist
		if not "character" in getData or len(getData["character"]) == 0 or xcharacter in open("Blacklist.txt", "r"):
			print("\n Character: {} Doesn't exist or BLACKLISTED".format(xcharacter))
		
		else:
			#Send ID to ESI for PublicData
			idCharacter = getData["character"][0]
			fetchPublic = requests.get("https://esi.evetech.net/latest/characters/{}".format(idCharacter), params = {"datasource": "tranquility"})
			getPublic = fetchPublic.json()
			idCorporation = getPublic["corporation_id"]
			idName = getPublic["name"]
			#sorttrue
			if str(idCorporation) in NPCcorporation:
				print("{}/{}".format(numPlist, numPilot), "ID:", idCharacter, "| Name:", idName, "| Corporation:", idCorporation, "| NPC Corporation: True")
				#<font size="12" color="#bfffffff"></font><font size="12" color="#ffd98d00"><loc><a href="showinfo:1386//97143141">01 Chaos</a></font><font size="12" color="#bfffffff">,</loc></font>
				results.writelines('\n<font size="12" color="#bfffffff"></font><font size="12" color="#ffd98d00"><loc><a href="showinfo:1386//{}">{}</a></font><font size="12" color="#bfffffff">,</loc></font>'.format(idCharacter, idName))
				blacklist.write("{}\n".format(idName))
				newlineappend +=1 #check

			#sortfalse
			else:
				print("{}/{}".format(numPlist, numPilot), "ID:", idCharacter, "| Name:", idName, "| Corporation:", idCorporation, "| NPC Corporation: False")
			
			#spaced every 50th lines
			if newlineappend == 50:
				newlineappend = 0
				results.writelines("\n\n STOP COPYING [50th Pilot in set] \n\n")

			if numPlist == numPilot:
				results.close()
				blacklist.close()

#-------------------##MAIN###-------------------#
while True:
	cinput = input("----TYPE help FOR CMDS---- \n")



#---------------------[HELP]		
	if cinput == "send":
		postdiscordcmd()	

	if cinput == "help":
		print("\nrun - Filter Data to NPCCorporation [MAIN]\n\nexit - Close terminal\n\nconvertchartoid - [DEBUG]Convert Data to ID by ESI\n\nlistcharamount - # of Character in Data" )




#---------------------[LIST]
	if cinput == "listcharamount":
		ListChar = 0
		Charfile = open("CharacterData.txt", "r")
		with Charfile as CData:
			for nlines in CData:
				ListChar += 1
		print("There is", ListChar, "character loaded in dataset.")



#---------------------[run]
	if cinput == "run":
		manualsort()






#---------------------[CHARID]
	if cinput == "convertchartoid":
		ListChar = 0
		Charfile = open("CharacterData.txt", "r")
		with Charfile as CData:
			for nlines in CData:
				ListChar += 1
	
	#EsiBulk check only allow 1000 to be scanned at once. I'll figure out later.		
		if ListChar > 1001:
			print("Due to ESI limitation, and Karulean lazy. Please reduce it down to 1000 character to process.")


		else:
			print("\nThere is", ListChar, "character loaded in dataset.")
			converttoids()




#---------------------[FilterCommands]
	if cinput == "filtertonpc":
		filteresicorp()

	


#---------------------[EXIT]	
	if cinput == "exit":
		break
		sys.exit()
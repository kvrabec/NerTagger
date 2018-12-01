import re
import urllib
import tqdm
import requests
import json
import time
import os
import string
import pandas
from nltk import tokenize
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson.objectid import ObjectId

#database strings
connString = "mongodb://localhost:27017"
qaDataDatabse = "qaData"
footballDataCollection = "footballData"
otherDataCollection = "otherData"
keywordsCollection = "keywords"
sleepTime = 60

#api strings

apiKey = "fccf51f33e084372880afbd20d49659e"
apiUrl = "http://api.football-data.org/v2/"

##################################################   PUBLIC METHODS   ##############################################

def downloadDataFromWiki(linksFile):
    client = MongoClient(connString)
    db = client[qaDataDatabse]

    if not _checkIfFilesExist([linksFile]):
            return

    lines = [line.rstrip('\n') for line in open(linksFile)]

    for line in tqdm.tqdm(lines,
                            total=len(lines),
                            unit_scale=True, unit=" articles",
                            desc="Downloading text from wikipedia"):

            if db[footballDataCollection].find({"link" : line}).count() > 0:
                    continue
            wikiUrl = line
            html = urllib.request.urlopen(wikiUrl).read()
            soup = BeautifulSoup(html,"html5lib")
            alltext = ""
            paragraphs = soup.findAll('p')
            for paragraph in tqdm.tqdm(paragraphs,
                                            total=len(paragraphs),
                                            unit_scale=True, unit=" paragraphs",
                                            desc="Parsing paragraphs"):
                    text = ''.join(paragraph.findAll(text = True))
                    if text.isspace() or text == '':
                            continue
                    text = re.sub(r"\[.*?\]","", text.strip())
                    if(alltext == ""):
                            text = re.sub(r" \([^\)]*\)","", text)
                    alltext += text + " "

            headingNameText = soup.find('h1').findAll(text = True)

            db_paragraph = {
                            "link" : line,
                            "heading_Name" : headingNameText[0],
                            "text" : alltext,
                            }
            db[footballDataCollection].insert_one(db_paragraph)

def getKeywordsFromAPI():

    def _checkIfApiLimitExcided(apiRequestCounter, sleepTime):
            if apiRequestCounter % 10 == 0 and apiRequestCounter > 0 :
                    print("Max requests per minute is 10. Sleping for " +  str(sleepTime) + " seconds")
                    for i in tqdm.tqdm(range(sleepTime,0,-1),
                                                    total=sleepTime,
                                                    unit_scale=True, unit=" secounds",
                                                    desc="Countdown for API request limit"):
                            time.sleep(1)

    client = MongoClient(connString)
    db = client[qaDataDatabse]
                            
    idlist = ["2000","2001","2002","2003","2014","2015","2019","2021"]

    apiRequestCounter = 0

    for id in tqdm.tqdm(idlist,total=len(idlist),
                            unit_scale=True, unit=" competitons",
                            desc="Loading competitions from API"):
            _checkIfApiLimitExcided(apiRequestCounter, sleepTime)
            url = apiUrl + "competitions/" + id + "/teams"
            response = requests.get(url, headers={"X-Auth-Token" : apiKey})
            content = json.loads(response.content)
            if "message" in content and "errorCode" in content and re.match(r"You reached your request limit. Wait [0-9]+ seconds.", content["message"]):
                    waitTime = re.findall(r"\d+", content["message"])
                    _checkIfApiLimitExcided(apiRequestCounter + 10, int(waitTime[0]) + 1)
                    response = requests.get(url, headers={"X-Auth-Token" : apiKey})
                    content = json.loads(response.content)
            competition = content["competition"]["name"]
            if db[keywordsCollection].find({"type" : "competition", "text" : competition}).count() == 0:
                    db[keywordsCollection].insert_one({
                                                    "type" : "competition",
                                                    "text" : competition
                                                    })
            else:
                    continue
            apiRequestCounter += 1
            teams = content["teams"]
            for team in tqdm.tqdm(teams,total=len(teams),
                                                    unit_scale=True, unit=" teams",
                                                    desc="Loading teams from API from " + content["competition"]["name"]):
                    fullTeamName = team["name"]
                    shortTeamName = team["shortName"]
                    if db[keywordsCollection].find({"type" : "team", "text" : fullTeamName}).count == 0:
                            db[keywordsCollection].insert_one({
                                                            "type" : "team",
                                                            "text" : fullTeamName
                                                            })

                    _checkIfApiLimitExcided(apiRequestCounter)
                    _getPlayersForTeam(team)
                    apiRequestCounter += 1

def mongoParagraphsToFiles(tokenFilePath, trainWikiIDsFilePath, testWikiIDsFilePath, filesPath):
    client = MongoClient(connString)
    db = client[qaDataDatabse]
    
    tokenFile = open(tokenFilePath, "w+", encoding = "utf-8")
    
    trainWikiIdFile = open(trainWikiIDsFilePath, "w+", encoding = "utf-8")
    testWikiIdFile = open(testWikiIDsFilePath, "w+", encoding = "utf-8")

    footballData = db[footballDataCollection].find()
    dataLen = db[footballDataCollection].count()
    index = 0
    for line in tqdm.tqdm(footballData,total=dataLen,
                            unit_scale=True, unit=" articles",
                            desc="Saving articles to files"):
            f = open(filesPath + str(line["_id"]) + ".txt","w+", encoding="utf-8")
            alltext = line["text"]
            text = tokenize.sent_tokenize(alltext)
            sentenceCount = len(text)
            counter = 1
            for sentence in text:
                    f.write(sentence)
                    if counter < sentenceCount:
                             f.write("\n\n")
                    counter += 1
            tokenizedText = tokenize.word_tokenize(alltext)
            for word in tokenizedText:
                    if word.isalnum() or "-" in word:
                            tokenFile.write(word.lower() + " ")

            if index <= (dataLen*0.7):
                    trainWikiIdFile.write(str(line["_id"]) + ".txt\n")
            else:
                    testWikiIdFile.write(str(line["_id"]) + ".txt\n")
            index += 1
            f.close() 
    trainWikiIdFile.close()
    testWikiIdFile.close()
    tokenFile.close()

def generateTokensFileAndArticleIdsFiles(wikiDataCsvFile, tokenFilePath, trainWikiIDsFilePath, testWikiIDsFilePath):

    def getArticleIdList(wikiDataCsvFile):
            result =  pandas.read_csv(wikiDataCsvFile,
                        encoding="utf-8",
                        keep_default_na=False)
            idList = []
            for row in result.itertuples():
                    if row.id not in idList:
                            idList.append(row.id)
            return idList
            

    distinctAritcleIDList = getArticleIdList(wikiDataCsvFile)
    distinctIDLen = len(distinctAritcleIDList)
    trainAritcleIds = distinctAritcleIDList[:int(distinctIDLen * 0.7)]
    testArticleIds = distinctAritcleIDList[int(distinctIDLen * 0.7):]
    
    tokenFile = open(tokenFilePath, "w+", encoding = "utf-8")
    
    trainWikiIdFile = open(trainWikiIDsFilePath, "w+", encoding = "utf-8")
    testWikiIdFile = open(testWikiIDsFilePath, "w+", encoding = "utf-8")

    footballData = getAllArticles()
    dataLen = footballData.count()

    otherData = getAllOtherData()
    otherDataLen = otherData.count()

    for line in tqdm.tqdm(footballData,total=dataLen,
                            unit_scale=True, unit=" football articles",
                            desc="Generating token, and articleId files"):
            alltext = line["text"]
            articleID = str(line["_id"])
            if articleID not in distinctAritcleIDList:
                continue
            tokenizedText = tokenize.word_tokenize(alltext)
            for word in tokenizedText:
                    if word.isalnum() or "-" in word:
                            tokenFile.write(word.lower() + " ")

            if articleID in trainAritcleIds:
                    trainWikiIdFile.write(str(line["_id"]) + "\n")
            elif articleID in testArticleIds:
                    testWikiIdFile.write(str(line["_id"]) + "\n")
            else:
                    print("WARNING: ArticleID '" + str(articleID) + "' is not in train or test id list!")

    for line in tqdm.tqdm(otherData,total=otherDataLen,
                            unit_scale=True, unit=" other articles",
                            desc="Generating token, and articleId files"):
            alltext = line["text"]
            articleID = str(line["_id"])
            if articleID not in distinctAritcleIDList:
                continue
            tokenizedText = tokenize.word_tokenize(alltext)
            for word in tokenizedText:
                    if word.isalnum() or "-" in word:
                            tokenFile.write(word.lower() + " ")

            if articleID in trainAritcleIds:
                    trainWikiIdFile.write(str(line["_id"]) + "\n")
            elif articleID in testArticleIds:
                    testWikiIdFile.write(str(line["_id"]) + "\n")
            else:
                    print("WARNING: ArticleID '" + str(articleID) + "' is not in train or test id list!")

    trainWikiIdFile.close()
    testWikiIdFile.close()
    tokenFile.close()

def generateDataCsvFile(wikiDataCsvFile, questionsFile):

    if not _checkIfFilesExist([questionsFile]):
            return
    dir = os.path.dirname(wikiDataCsvFile)
    if not os.path.exists(dir):
            os.mkdir(dir)

    data = open(wikiDataCsvFile, "w+", encoding="utf-8")
    alltext = "id,questions,answer_char_index_ranges,answer_token_index_ranges\n"
    questions = open(questionsFile, "r", encoding="utf-8").readlines()
    articleId = ""
    for line in tqdm.tqdm(questions,
                            total=len(questions),
                            unit_scale=True, unit=" articles",
                            desc="Generating wikidataCsv file from questions"):
            split = line.split(',')
            if articleId == "":
                    questions = []
                    answerIndexRanges = []
                    answerTokenIndexRanges = []
                    articleId = split[0]
                    articleText = getArticleTextById(articleId)

            if not articleId == split[0]:
                    alltext += articleId + "," + "\"" + "|".join(questions) + "\"" + ","  + "\"" + ",".join(answerIndexRanges) + "\"" + "," + "\"" + ",".join(answerTokenIndexRanges) + "\"\n"
                    articleId = split[0]
                    articleText = getArticleTextById(articleId)
                    questions = []
                    answerIndexRanges = []
                    answerTokenIndexRanges = []

            question = split[1]
            answer = split[2].replace('\n','')
            startAnswerIndex = _findFirst(articleText,answer)
            endAnswerIndex = startAnswerIndex + len(answer)
            answerIndexRange = str(startAnswerIndex) + ":" + str(endAnswerIndex) 
            tokenizedText = tokenize.word_tokenize(articleText)
            tokenizedAnswer = tokenize.word_tokenize(answer)
            answerTokenIndexRange = _findTokenRange(tokenizedText, tokenizedAnswer)

            questions.append(question)
            answerIndexRanges.append(answerIndexRange)
            answerTokenIndexRanges.append(answerTokenIndexRange)
                    
    alltext += articleId + "," + "\"" + "|".join(questions) + "\"" + ","  + "\"" + ",".join(answerIndexRanges) + "\"" + "," + "\"" + ",".join(answerTokenIndexRanges) + "\"\n"

    data.write(alltext)
    data.close()

def readPublicQaData(filePath, wikiDataCsvFile):
    client = MongoClient(connString)
    db = client[qaDataDatabse]

    file = open(filePath, "r", encoding="utf-8")
    wikiData = open(wikiDataCsvFile, "a", encoding="utf-8")

    parsedData = json.load(file)["data"]

    for data in tqdm.tqdm(parsedData, total=len(parsedData), 
                             desc="Reading public QA data", unit_scale=True,
                             unit=" articles"):
        counter = 0
        headingNameText = data["title"]
        for dataRow in data["paragraphs"]:
            articleText = dataRow["context"]
            db_paragraph = {
                                "heading_Name" : headingNameText + "_" + str(counter),
                                "text" : articleText,
                                }
            if db[otherDataCollection].find(db_paragraph).count() == 0:
                db[otherDataCollection].insert_one(db_paragraph)
            articleID = db[otherDataCollection].find_one(db_paragraph)["_id"]
            questions = []
            answerIndexRanges = []
            answerTokenIndexRanges = []

            for qaPair in dataRow["qas"]:
                question = qaPair["question"].replace("\"", "'")
                if qaPair["is_impossible"] == True:
                    answer = qaPair["plausible_answers"][0]["text"]
                    answerIndexRange = qaPair["plausible_answers"][0]["answer_start"]
                else:
                    answer = qaPair["answers"][0]["text"]
                    answerIndexRange = qaPair["answers"][0]["answer_start"]
                answerIndexRangeString = str(answerIndexRange) + ":" + str(answerIndexRange + len(answer))
                tokenizedText = tokenize.word_tokenize(articleText)
                tokenizedAnswer = tokenize.word_tokenize(answer)
                answerTokenIndexRange = _findTokenRange(tokenizedText, tokenizedAnswer)
                questions.append(question)
                answerIndexRanges.append(answerIndexRangeString)
                answerTokenIndexRanges.append(answerTokenIndexRange)

            counter += 1
            wikiData.write(str(articleID) + "," + "\"" + "|".join(questions) + "\"" + ","  + "\"" + ",".join(answerIndexRanges) + "\"" + "," + "\"" + ",".join(answerTokenIndexRanges) + "\"\n")
       


def removeDuplicates(filenames):
    client = MongoClient(connString)
    db = client[qaDataDatabse]
    for filename in filenames:
            print("Removing duplicates for " + filename)
            linesSeen = set()
            inFileName = filename
            outFileName = filename[:-4] + "_cleared" + ".txt"
            outfile = open(outFileName, "w+", encoding="utf-8")
            for line in open(inFileName, "r", encoding="utf-8"):
                    if line.lower() not in linesSeen and not line.isspace() and line != "": 
                            outfile.write(line.replace("\n","").replace("\r","") + " ")
                            linesSeen.add(line.lower())
            outfile.close()

def concatKeywordsWithTokenFile(tokenFilePath):

    if not _checkIfFilesExist([tokenFilePath]):
    	return

    print("Concating token file with keywords")
    tokenFile = open(tokenFilePath, "a", encoding="utf-8")
    for keyword in getAllKeywords():
    	tokenFile.write(keyword["text"].lower() + " ")
    tokenFile.close()

def getAllKeywords():
    client = MongoClient(connString)
    db = client[qaDataDatabse]
    return db[keywordsCollection].find()
    
def getArticleById(articleID):
    client = MongoClient(connString)
    db = client[qaDataDatabse]
    return db[footballDataCollection].find_one({"_id" : ObjectId(articleID)})

def getArticleTextById(articleID):
    client = MongoClient(connString)
    db = client[qaDataDatabse]
    article = db[footballDataCollection].find_one({"_id" : ObjectId(articleID)})
    if article:
        return article["text"]
    else:
        article = db[otherDataCollection].find_one({"_id" : ObjectId(articleID)})
        return article["text"]

def getAllArticles():
    client = MongoClient(connString)
    db = client[qaDataDatabse]
    return db[footballDataCollection].find()

def getAllOtherData():
    client = MongoClient(connString)
    db = client[qaDataDatabse]
    return db[otherDataCollection].find()


##################################################   PRIVATE METHODS   ##############################################

def _getPlayersForTeam(team):
    client = MongoClient(connString)
    db = client[qaDataDatabse]

    url = apiUrl + "/teams/" + str(team["id"])
    response = requests.get(url, headers={"X-Auth-Token" : apiKey})
    content = json.loads(response.content)
    players = content["squad"]
    for player in tqdm.tqdm(players,
                            total=len(players),
                            unit_scale=True, unit=" players",
                            desc="Loading players for " + content["name"]):
            playerName = player["name"]
            if db[keywordsCollection].find({"type" : "player", "text" : playerName}).count() == 0:
                    db[keywordsCollection].insert_one({
                                                    "type" : "player",
                                                    "text" : playerName
                                                    })

def _findAll(text, string):
    start = 0

    while True:
            start = text.find(string, start)
            if start == -1: return
            yield start
            start += len(string) 

def _findFirst(text, string):
    index = 0
    if string in text:
            c = string[0]
            for ch in text:
                    if ch == c:
                            if text[index:index + len(string)] == string:
                                    return index
                    index += 1
    return -1

def _findWordByIndexRange(indexRange, text):
    split = indexRange.split(":")
    start = int(split[0])
    end = int(split[1])
    return text[start:end]

def _findLine(text, string):
    counter = 0

    for line in text.split("\n"):
            if string in line:
                    return counter
            counter += 1

def _checkIfFilesExist(files):
    for file in files:
            if not os.path.exists(file):
                    print("Links file not found at '" + os.path.dirname(os.path.realpath(__file__)) + file + "'")
                    return False

    return True

def _findTokenRange(text, string):
    wordCount = len(string)
    for index, word in enumerate(text):
                    if wordCount == 1 and word == string[0]:
                            return str(index) + ":" + str(index + 1)
                    elif wordCount > 1:
                            counter = 0
                            for answerWord in string:
                                    textLen = len(text)
                                    if (index + counter) >= textLen:
                                            return "-1:-1"
                                    if text[index + counter] == answerWord:
                                            counter += 1
                                    else:
                                            break
                            if counter == wordCount:
                                    return str(index) + ":" + str(index + wordCount)
    return "-1:-1"

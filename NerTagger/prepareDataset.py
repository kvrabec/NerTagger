import json
import csv
import os
import re
import codecs
import tqdm

folderPath = 'classificationData'
train = 80
test = 20

def appendToRowAttribute(array, row, attribute):
    if attribute in row:
        data = row[attribute]
        appendToArray(array, data)

def appendToRowIndex(array, row, index):
    if index != -1 and index < len(row):
        data = row[index]
        appendToArray(array, data)

def appendToArray(array, data):
    if data not in array:
            if not re.match(r'(Q[0-9]{5,10})', data) and not re.match(r'(t[0-9]{5,10})', data):
                array.append(data)

def backupDataset(dataset, datasetFilePath):
    with codecs.open(datasetFilePath, 'w', encoding='utf-8') as outfile:
        json.dump(dataset, outfile, ensure_ascii=False)

def splitDataset(dataset, train, test):
    trainDataset = {}
    testDataset = {}

    for key in dataset.keys():
        itemCount = len(dataset[key])
        trainCount = (train* itemCount)//100
        trainDataset.update({key : dataset[key][:trainCount]})
        testDataset.update({key : dataset[key][trainCount:]})

    return trainDataset, testDataset


def getDataset(datasetPath, wikiDataset, fmDataset, split = False, generateNewDataset = False):

    datasetFilePath = folderPath + '/' + datasetPath
    if os.path.isfile(datasetFilePath) and not generateNewDataset:
        with open(datasetFilePath, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
            if split:
                return splitDataset(dataset, train, test)
            return dataset

    teams = []
    persons = []
    competitions = []
    countries = []
    stadiums = []

    with open(folderPath + '/' + wikiDataset, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for dataRow in tqdm.tqdm(data,
                        total=len(data),
                        unit_scale=True, unit=" rows",
                        desc="Reading wikipedia dataset"):
        appendToRowAttribute(teams, dataRow, 'clubLabel')
        appendToRowAttribute(persons, dataRow, 'head_coachLabel')
        appendToRowAttribute(competitions, dataRow, 'leagueLabel')
        appendToRowAttribute(countries, dataRow, 'countryLabel')
        appendToRowAttribute(persons, dataRow, 'chairpersonLabel')
        appendToRowAttribute(stadiums, dataRow, 'home_venueLabel')

    num_lines = sum(1 for line in open(folderPath + '/' + fmDataset, encoding='utf-8'))

    with open(folderPath + '/' + fmDataset, 'r', encoding='utf-8') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        csv_file.seek(0,0)
        for row in tqdm.tqdm(data,
                        total=num_lines-1,
                        unit_scale=True, unit=" rows",
                        desc="Reading Football Manager dataset"):
            appendToRowIndex(persons, row, 1)

    print('clubs: ' + str(len(teams)) + '\ncoaches: ' + str(len(persons)) + '\nleagues: ' + str(len(competitions)) + '\ncountries: ' + str(len(countries))  + '\nsponsors: ' + str(len(sponsors)) + '\nstadiums: ' + str(len(stadiums)))

    dataset = {
        'clubs' : teams,
        'persons' : persons, 
        'leagues' : competitions,
        'countries' : countries, 
        'sponsors' : sponsors, 
        'stadiums' : stadiums
        }

    backupDataset(dataset, datasetFilePath)

    return dataset
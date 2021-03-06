import sqlite3
import operator

import sys, os

from .AddScoresToDatabase import getTitle
from .AddScoresToDatabase import getDate
from .InitDatabase import getRedditInstance
from .AddScoresToDatabase import getSubmissionDateFromDatabase

# Create a table with the rankings from the local database for a series up until a specific submission excluding that submission
def getRankingsFromDatabase(submission):
    
    # Connect to database
    database = sqlite3.connect(os.path.join(os.path.dirname(__file__), "database.db"))
    cursor = database.cursor()

    # Create a set with all the usernames in that series
    nameSet = set()
    for row in cursor.execute("SELECT Place1, Place2, Place3 FROM ChallengeRankings WHERE SeriesTitle = ? AND Date < ?", [getTitle(submission), str(getSubmissionDateFromDatabase(submission))]):
        for val in row:
            if val is not '':
                for author in val.split('|'):
                    nameSet.add(author)
                
    nameList = [name for name in nameSet]

    table = [[name, 0, 0, 0] for name in nameList]

    # Iterate through every post in the series and increment the winners in the table
    for i in range(1, 4):
        for row in cursor.execute("SELECT Place" + str(i) + " FROM ChallengeRankings WHERE SeriesTitle = ? AND Date < ?", [getTitle(submission), str(getSubmissionDateFromDatabase(submission))]):
            for val in row:
                if val is not '':
                    for author in val.split('|'):
                        table[nameList.index(author)][i] += 1

    table.sort(reverse = True, key = operator.itemgetter(1, 2, 3))

    database.close()

    #print(table)
    return table

def getTableOfSeriesGamesFromDatabase(SeriesTitle):

    # Connect to database
    database = sqlite3.connect(os.path.join(os.path.dirname(__file__), "database.db"))
    cursor = database.cursor()

    table = []

    for row in cursor.execute("SELECT SubmissionID, SubmissionTitle, Place1, Place2, Place3 FROM ChallengeRankings WHERE SeriesTitle = ?", [SeriesTitle]):
        table.append(row)

    database.close()

    #print(table)
    return table

if __name__ == '__main__':
    #reddit = getRedditInstance()
    #print(getRankingsFromDatabase(reddit.submission(id = '6fe4fi')))
    print(getTableOfSeriesGamesFromDatabase("roadslesstravelled"))
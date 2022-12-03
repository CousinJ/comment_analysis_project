from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()


#video Id 
videoId = 'H9AAnV59ddE'
youtube_service_object = build('youtube', 'v3', developerKey=os.getenv('API_KEY'))


totalComments = []
postingUsers = []
#function gets comments information by iterating through items of comment threads.
def loadText(response):
    for item in response['items']:
        comment = item['snippet']['topLevelComment']
        user = comment['snippet']['authorDisplayName']
        commentText = comment['snippet']['textDisplay']

        totalComments.append(commentText)

#function returns the comment thread on a page given the page parmeter
def getCommentThreads(page):
    request = youtube_service_object.commentThreads().list(part='snippet', videoId=videoId, maxResults=100, textFormat='plainText', pageToken=page)
    response = request.execute()
    return response
    


#getting text from the function for the FIRST TIME
commentHelper = getCommentThreads('')
next_page_token = commentHelper['nextPageToken']
loadText(commentHelper)

try:
    while next_page_token:
        commentHelper = getCommentThreads(next_page_token)
        next_page_token = commentHelper['nextPageToken']
        loadText(commentHelper)
except:
    print(len(totalComments))






    
from googleapiclient.discovery import build
import os
import re
from dotenv import load_dotenv
load_dotenv()


regex = re.compile('[,\.!?]')
#video Id 
videoId = 'H9AAnV59ddE'
youtube_service_object = build('youtube', 'v3', developerKey=os.getenv('API_KEY'))
#sorts through list of dicts based on likes 



commentStats = []

#function gets comments information by iterating through items of comment threads.
def loadText(response):
    for item in response['items']:

        comment = item['snippet']['topLevelComment']
        user = comment['snippet']['authorDisplayName']
        commentText = comment['snippet']['textDisplay']
        commentLikes = comment['snippet']['likeCount']
        commentReplies = item['snippet']['totalReplyCount']

        commentDict = dict(user = user, text = commentText, likes = commentLikes, replies= commentReplies)
        commentStats.append(commentDict)
      

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
   
    print('done')


#sorting the comment stats via likes numbers
sortedByLikes = sorted(commentStats, key=lambda dict: dict['likes'], reverse=True)

# for item in sortedByLikes:

#     # print('==============\n', item['user'], "\n", item['text'], '\n', item['likes'], '\n')


#take first 100 top comments (but make that number changeable) and save to a new list called top.
#take the rest and save those to a new list called lesser
top_comments = []
lesser_comments = []

def topCommentGetter(top_x):
    for x in range(top_x):
        top_comments.append(sortedByLikes[x])

    for x in range(top_x, len(sortedByLikes)):
        lesser_comments.append(sortedByLikes[x])
    
    

    
    
   


topCommentGetter(10)






def clean_comments():
    #clean comments
    top_cmnts_clean = []
    for item in top_comments:
        clean_item = item['text'].casefold()
        clean_item = regex.sub('', clean_item)
        top_cmnts_clean.append(clean_item.split(' '))
    lesser_cmnts_clean = []
    for item in lesser_comments:
        clean_item = item['text'].casefold()
        clean_item = regex.sub('', clean_item)
        lesser_cmnts_clean.append(clean_item.split(' '))
   







from googleapiclient.discovery import build
import os
import re
from dotenv import load_dotenv

load_dotenv()




youtube_service_object = build('youtube', 'v3', developerKey=os.getenv('API_KEY'))



#function returns the comment thread on a page given the page parmeter and video parameter

def getCommentThreads(page, video_Id):
    request = youtube_service_object.commentThreads().list(part='snippet', videoId=video_Id, maxResults=100, textFormat='plainText', pageToken=page)
    response = request.execute()
    return response
#

#function gets comments information by iterating through items of comment threads. returns unit of dictionary.* append to a list*
def loadText(response):
    for item in response['items']:

        comment = item['snippet']['topLevelComment']
        user = comment['snippet']['authorDisplayName']
        commentText = comment['snippet']['textDisplay']
        commentLikes = comment['snippet']['likeCount']
        commentReplies = item['snippet']['totalReplyCount']

        commentDict = dict(user = user, text = commentText, likes = commentLikes, replies= commentReplies)
        return commentDict
#
#this funciton takes in the array of dictionaires  (usually will be blank list)  and sorts them by the number of likes. the top x is the number of top comments. the rest will be sorted into lesser comments.
def top_lesser_sorter(comment_stats_dict):
    top_comments = []
    lesser_comments = []

    sortedByLikes = sorted(comment_stats_dict, key=lambda dict: dict['likes'], reverse=True)
    def topCommentGetter(top_x):
        
        for x in range(top_x):
            top_comments.append(sortedByLikes[x])

        for x in range(top_x, len(sortedByLikes)):
            lesser_comments.append(sortedByLikes[x])   
    #calling the top comment getter with arg num.
    topCommentGetter(10)
    return top_comments, lesser_comments
#





#this is is the start of the process by using the two functionsGETCOMMENTTHREADS and LOADTEXT and do the try/except to start with no page and iterate through other pages.
def initializePage():
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


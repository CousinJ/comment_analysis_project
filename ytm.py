#YOUTUBE METHODS
from googleapiclient.discovery import build
import os


from dotenv import load_dotenv

load_dotenv()

youtube_service_object = build('youtube', 'v3', developerKey=os.getenv('API_KEY'))
# 
# #get comment thread response. params: video_id, page. returns the response
def get_response(page, video_Id):
    request = youtube_service_object.commentThreads().list(part='snippet', videoId=video_Id, maxResults=100, textFormat='plainText', pageToken=page)
    response = request.execute()
    return response

# #extract Item. params: response returns a dictionary of extracted values
def extract_item(response, array):
    for item in response['items']:

        comment = item['snippet']['topLevelComment']
        user = comment['snippet']['authorDisplayName']
        commentText = comment['snippet']['textDisplay']
        commentLikes = comment['snippet']['likeCount']
        commentReplies = item['snippet']['totalReplyCount']

        commentDict = dict(user = user, text = commentText, likes = commentLikes, replies= commentReplies)
        array.append(commentDict)
    
  


def get_topComments(top_x, sorted_by_likes):
    top_comments = []
    lesser_comments = []
    for x in range(top_x):
        top_comments.append(sorted_by_likes[x])

    for x in range(top_x, len(sorted_by_likes)):
        lesser_comments.append(sorted_by_likes[x])    
    return  top_comments
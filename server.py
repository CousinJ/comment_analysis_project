from flask import Flask, redirect, url_for, render_template,request
import ytm 
app = Flask(__name__)

comment_dict_array = []

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        #getting vars from user
        youtube_video_id = request.form.get('youtube_video_id')
        top_comment_num = request.form.get('top_comment_num')
        top_comment_num = int(top_comment_num)

        print(youtube_video_id)
        print(top_comment_num)
        
        
       
        res = ytm.get_response('', youtube_video_id)
        ytm.extract_item(res, comment_dict_array)
        

        next_page = res['nextPageToken']
        res=ytm.get_response(next_page, youtube_video_id)
        ytm.extract_item(res, comment_dict_array)
        
        x = 0
        
        try:
            while len(list(next_page)) > 10:
                next_page = res['nextPageToken']
                res=ytm.get_response(next_page, youtube_video_id)
                ytm.extract_item(res, comment_dict_array)
                x += 1
                print(x)
        except: 
            print('all pages have been processed')

            cda_sortedByLikes = sorted(comment_dict_array, key=lambda dict: dict['likes'], reverse=True)
            sorted_topx_result = ytm.get_topComments(top_comment_num, cda_sortedByLikes)
            
            
            print(sorted_topx_result)
        
      
        

    
    return render_template('home.html')


if __name__ == '__main__':
    app.run()




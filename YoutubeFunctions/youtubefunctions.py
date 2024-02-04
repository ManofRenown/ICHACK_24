from googleapiclient.discovery import build
import os

api_key = os.getenv('YT_API_KEY')
api_service_name = 'youtube'
api_version = 'v3'

youtube = build(api_service_name, api_version, developerKey=api_key)


"""generate a url for each query"""
def generate_urls(list_of_queries, num_queries):
    
    urls = []
    for i in range(num_queries):
        if i < len(list_of_queries):
            urls.append(generate_url(list_of_queries[i]))

    return urls
    

def generate_url(query):
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=5,
        type='video',
        videoDuration = 'medium',
        videoEmbeddable = 'true',
        order = 'relevance'
    )

    response = request.execute()

    if len(response['items']) > 0:
        return ('https://www.youtube.com/watch?v=' + response['items'][0]['id']['videoId'], response['items'][0]['snippet']['thumbnails']['maxres']['url'], response['items'][0]['snippet']['title'])
    else:
        print("no search results for this query: ", query)
        return ("","","")

#print("\n\n")
#print(generate_url("How is cricket related to business"))

"""response = request.execute()



for item in response['items']:
    print("title: ", item['snippet']['title'])
    print("description: ", item['snippet']['description'])
    print("url: ",'https://www.youtube.com/watch?v=' + item['id']['videoId'])
    print('\n')"""
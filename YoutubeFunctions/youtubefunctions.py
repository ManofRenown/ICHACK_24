from googleapiclient.discovery import build

api_key = 'AIzaSyAwTMN48200ehT62T4kwuXw6ru5sKQPsG0'
api_service_name = 'youtube'
api_version = 'v3'

youtube = build(api_service_name, api_version, developerKey=api_key)

query = "i like socks"

request = youtube.search().list(
    q=query,
    part="snippet",
    maxResults=10
)

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
        maxResults=1,
        type='video',
        videoDuration = 'medium',
        videoEmbeddable = 'true',
        order = 'relevance'
    )

    response = request.execute()
    #print(response)
    return 'https://www.youtube.com/watch?v=' + response['items'][0]['id']['videoId']

print("\n\n")
print(generate_url("Chinese youth slang rùn meaning to flee"))

"""response = request.execute()



for item in response['items']:
    print("title: ", item['snippet']['title'])
    print("description: ", item['snippet']['description'])
    print("url: ",'https://www.youtube.com/watch?v=' + item['id']['videoId'])
    print('\n')"""
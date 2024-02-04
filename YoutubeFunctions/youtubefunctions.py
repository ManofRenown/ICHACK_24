from googleapiclient.discovery import build

api_key = 'AIzaSyDaYiSldkshg_pVfJZL37DjKRlKQo7AVX8'
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
    
    for search_result in response.get('items', []):
        # Access the snippet data for each search result
        snippet = search_result.get('snippet', {})
        title = snippet.get('title')
        thumbnails = snippet.get('thumbnails', {})
        default_thumbnail_url = thumbnails.get('default', {}).get('url')
        #print("Here is the new method for this", title,default_thumbnail_url)

    thumbnails = response['items'][0]['snippet']['thumbnails']
    #print(response)
    return ('https://www.youtube.com/watch?v=' + response['items'][0]['id']['videoId'], thumbnails['default']['url'])

print("\n\n")
print(generate_url("Chinese youth slang rùn meaning to flee"))

"""response = request.execute()



for item in response['items']:
    print("title: ", item['snippet']['title'])
    print("description: ", item['snippet']['description'])
    print("url: ",'https://www.youtube.com/watch?v=' + item['id']['videoId'])
    print('\n')"""
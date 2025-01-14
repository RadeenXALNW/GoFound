import scrapetube

def get_video_link(video_id, is_short=False):
    if is_short:
        return f"https://www.youtube.com/shorts/{video_id}"
    return f"https://www.youtube.com/watch?v={video_id}"

videos = scrapetube.get_search("health and nutrition")

for video in videos:
    video_id = video['videoId']
    # Check if it's a short video by looking at the navigationEndpoint
    is_short = 'reelWatchEndpoint' in video['navigationEndpoint']
    
    video_link = get_video_link(video_id, is_short)
    print(f"Title: {video['title']['runs'][0]['text']}")
    print(f"Link: {video_link}")
    print("-" * 50)
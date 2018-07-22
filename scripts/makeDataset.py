"""
Dependencies:
1. Install the Google API client library for Python
	pip install --user google-api-python-client

2. Create a project in Google API dashboard. Get the API key. Enable YoutubeDataAPI in the project.

Documentation:
1. Google API client library: https://developers.google.com/api-client-library/python/start/installation
2. Youtube Data API: https://developers.google.com/youtube/v3/getting-started#quota
3. Youtube Data API: https://developers.google.com/youtube/v3/docs/playlistItems/list

"""
from apiclient.discovery import build
import csv
import pandas as pd


"""
Functions:
"""
# Call the API's commentThreads.list method to list the existing comments
def get_comments(youtube, video_id):
	results = youtube.commentThreads().list(
	part="snippet",
	videoId=video_id,
	).execute()
	comment_list = []
	for item in results["items"]:
		comment = item["snippet"]["topLevelComment"]
		text = comment["snippet"]["textOriginal"]
		comment_list.append(text)
	return comment_list

# def print_comemnts(results):
# 	for item in results["items"]:
# 		comment = item["snippet"]["topLevelComment"]
# 		text = comment["snippet"]["textOriginal"]
# 		print("%s" % text.encode('utf-8').strip()) ## How do we work with emojis?

def get_playlist_id(youtube, channel_id):
	results = youtube.channels().list(
			part = 'contentDetails',
			id = channel_id,
		).execute()
	playlist_id = results["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
	return playlist_id

def get_video_list(youtube, playlist_id):
	playlistRequest = youtube.playlistItems().list(
		playlistId = playlist_id,
		part = 'snippet',
		maxResults = 10,
		)
	video_id_list = []
	while playlistRequest:
		results = playlistRequest.execute()
		for item in results["items"]:
			video_id_list.append(item["snippet"]["resourceId"]["videoId"])
		playlistRequest = youtube.playlistItems().list_next(playlistRequest, results)
	return video_id_list


"""
Parameters
"""
key = "AIzaSyB6GUGFOHDWM--V-asJaEc2sK2tI8NdGSg"
youtube = build('youtube', 'v3', developerKey=key)
channel_id = 'UClj0L8WZrVydk5xKOscI6-A' ## Mercedez-Benz


"""
Run code
"""
playlist_id = get_playlist_id(youtube, channel_id)
video_id_list = get_video_list(youtube, playlist_id)
comment_list = []
for video_id in video_id_list:
	comment_list.extend(get_comments(youtube, video_id))

"""
Save the text to csv file
"""
comment_list_encode = [c.encode('utf-8') for c in comment_list]
df = pd.DataFrame(comment_list_encode)
df.to_csv('comments.csv', index=False, header=False, chunksize=500)










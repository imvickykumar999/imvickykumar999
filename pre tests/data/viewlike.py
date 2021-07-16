# Import Module
from tkinter import *
from googleapiclient.discovery import build

def video_details():
	if "youtube" in video_url.get():
		video_id = video_url.get()[len("https://www.youtube.com/watch?v="):]
    elif "youtu" in video_url.get():
		video_id = video_url.get()[len("https://youtu.be/"):]
	else:
		video_id = video_url.get()

	# creating youtube resource object
	youtube = build('youtube','v3',developerKey='AIzaSyCcJX4qdbo9caqxZSKDmuBjNVWfvq8_Wcs')

	# retrieve youtube video results
	video_request=youtube.videos().list(
		part='snippet,statistics',
		id=video_id
	)

	video_response = video_request.execute()

	title = video_response['items'][0]['snippet']['title']
	likes = video_response['items'][0]['statistics']['likeCount']
	views = video_response['items'][0]['statistics']['viewCount']

	details.config(text=f"Title:- {title}\nLikes:- {likes}\nViews:- {views}")

# Create Object
root = Tk()

# Set Geometry
root.geometry("500x300")

# Add Label, Entry Box and Button

Label(root,text="Title, Views, Likes of YouTube Video", fg="blue",
	font=("Helvetica 20 bold"),relief="solid",bg="white").pack(pady=10)
Label(root,text="Enter video URL or ID", font=("10")).pack()

video_url = Entry(root,width=40,font=("15"))
video_url.pack(pady=10)

Button(root,text="Get Details" ,font=("Helvetica 15 bold"),command=video_details).pack()

details = Label(root,text="")
details.pack(pady=10)

# Execute Tkinter
root.mainloop()

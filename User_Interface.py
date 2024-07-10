import threading
from Queue import *
from Video import *
from Video_LinkFetch import *

def dld_video(vid_object):
        vid_object.download_video("C:/NON-OS/Programming/VS CODE FOLDERS/Python Progams/AI-ContentGEN2")
        vid_object.create_clips()
        dld_Queue.dequeue()


video = None
thread_count = 0


option = input("Please Choose an option: \n 1. Generate clips from trending videos \n\nChoice: ")

approved_links = []
video_objects = []

if option == '1':
    #Fetch Trending video links
        video_linksmeta = trend_vidlinksfetch()
        for video in video_linksmeta:
            video_objects.append(Video(video[0], video[1], video[2], video[3]))

dld_Queue = Queue(len(video_objects))

for video in video_objects:
        dld_vid_thread = threading.Thread(target=dld_video, args=(video,))
        saved = False
        approved_timestamps = []

        for otimestamp in video.get_timestamps():
            print(f"Timestamp - {otimestamp}")
            timestamp = otimestamp.split(':')
            print(timestamp)
            
            timestamp = int(timestamp[0])*60 + int(timestamp[-1])#convert to seconds
            sub_clip_link = f"{video.get_link()}&t={timestamp}s" #ADD to class
            print(video.get_title() + " - " + sub_clip_link) #ADD to class

            if input("\nKeep link? y/n\n") == 'y':
                approved_links.append(sub_clip_link)
                approved_timestamps.append(otimestamp)
                saved = True



        if saved:
            video.set_subcliptimes(approved_timestamps)
            dld_Queue.enqueue(video)

            if not dld_vid_thread.is_alive():
                dld_vid_thread.start()

        
    
#Combine audio and video
#Cur video segments
#Change video to phone format
#Add subtitles to video




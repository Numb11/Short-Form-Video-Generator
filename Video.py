from pytube import YouTube 
import os, threading
from moviepy.editor import *
from googleapiclient.discovery import build
from PIL import *


API_Key = "AIzaSyDJGl1zNWZR8XzbwIjk81XPGRWosK4wFp4"

class Video:
    def __init__(self, title, link, length, creator):
        self.title = title
        self.link = link
        self.length = length
        self.creator = creator
        self.id = link.split('=')[-1]
        self.save_path = ''
        self.subclip_timestamps = []

    def __analyse_transcript(self):
        pass

    def __analyse_comments(self):
        try:
            youtube = build("youtube","v3",developerKey=API_Key)

            request = youtube.commentThreads().list(
            part = "snippet",
            videoId = self.id,
            maxResults = 100
            )

            response = request.execute()

            for comment in response["items"]:
                temp_comment = (comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]).rstrip()
                temp_comment = (list(filter(lambda x:x if self.id in x else None, temp_comment.split())))
                if len(temp_comment)>0:
                    temp_comment = (temp_comment[0][temp_comment[0].index(">")+1:temp_comment[0].index("<")])
                    self.subclip_timestamps.append("".join(temp_comment))

        except:
            pass

    def get_timestamps(self):
        if len(self.subclip_timestamps) > 0:
            pass
        else:
            self.__analyse_comments()
        
        return self.subclip_timestamps


    def __download_audio(self, SAVE_PATH):
        yt = YouTube(self.link) 
        mp4_streams = yt.streams.filter(file_extension='mp4', only_audio=True, only_video = False, progressive=False)
        mp4_streams[0].download(output_path=SAVE_PATH)
        return True

    def __download_visual(self, SAVE_PATH):
        yt = YouTube(self.link) 
        mp4_streams = yt.streams.filter(file_extension='mp4', only_audio=False, only_video = True, progressive=False)
        mp4_streams[0].download(output_path=SAVE_PATH)
        return True

    def __combine_audio_visual(self, SAVE_PATH):
        audiofile_path = SAVE_PATH + "/audio_only"
        videofile_path = SAVE_PATH + "/video_only"

        title = "".join(list(filter(lambda x: " " if x == "|" else x, self.title)))
        if not(os.path.exists(f"{SAVE_PATH}/{title}.mp4")):
            audio_file = AudioFileClip(audiofile_path + f"/{title}.mp4")
            video_file = VideoFileClip(videofile_path + f"/{title}.mp4")
            video_file = video_file.resize(newsize=(1080,1920))
            video_file.audio = CompositeAudioClip([audio_file])
    
            video_file.write_videofile(f"{SAVE_PATH}/{title}.mp4")
            video_file.close()

    def download_video(self,SAVE_PATH):
        save_path = SAVE_PATH + "/Videos"

        if not os.path.exists(save_path):
            os.makedirs(save_path)
            os.makedirs(save_path + "/video_only")
            os.makedirs(save_path + "/audio_only")
            os.makedirs(save_path + "/clips")

        self.title = (self.title).replace("|", "")
        
        if not (os.path.exists(save_path + "/video_only") and os.path.exists(save_path + "/audio_only")):
            if self.__download_visual(save_path + "/video_only"):
                self.__download_audio(save_path + "/audio_only")
            else:
                return False

        self.__combine_audio_visual(save_path)
        self.save_path = save_path
        return True
        
    def create_clips(self):
        video = VideoFileClip(self.save_path+'/'+self.title+".mp4")
        count = 0
        for timestamp in self.subclip_timestamps:
            count = count+1
            timestamp = timestamp.split(':')
            seconds_start = int(timestamp[0])*60+int(timestamp[-1])
            clip = video.subclip(seconds_start, seconds_start+60)
            clip.write_videofile(f"{self.save_path}/clips/{self.title}{count}.mp4")


    def set_subcliptimes(self, times):
        self.subclip_timestamps = times

    def get_link(self):
        return self.link
        
    def get_title(self):
        return self.title
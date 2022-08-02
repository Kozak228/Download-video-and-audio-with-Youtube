from __future__ import unicode_literals
import youtube_dl
import yt_dlp
import os
import validators


def progress_hook(d):
	if (d['status'] == 'downloading'):
		print(f"{d['_speed_str']} ({d['_percent_str']})")


yt_opts = {
   'format' : 'mp4/bestaudio/best',
   'postprocessors' : [{
   'key' : 'FFmpegExtractAudio',
   'preferredcodec' : 'mp3',
   'preferredquality' : '192',
   }],
}

f = True

# while f:
# 	link = input("Вставь ссылку на видос -> ")
# 	if validators.url(link):
# 		f = False
# 		break
# 	else:
# 		print("Ошибка! Введена не ссылка!\n")

link = "https://www.youtube.com/watch?v=uO6Dzi_LWdU&t=5s"
linkPC = input("\nВставь путь куда скачать -> ")


if linkPC != "":
	os.chdir(linkPC)
else:
	os.chdir('D:\\Загрузки')

with yt_dlp.YoutubeDL(yt_opts) as ydl:
	f1 = ydl.download(link)

# print(f1)

# print(f"title: {f1.get('title')}\n ")
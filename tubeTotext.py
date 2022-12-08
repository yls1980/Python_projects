import requests
import moviepy.editor as mp
import speech_recognition as sr
from os import path
from pydub import AudioSegment
import io

fold = 'e:\\Python_projects\\MyProjects\\TubeToText\\'
file_name = 'videoplayback'
def video2mp3():
    fileswav = []
    clip = mp.VideoFileClip(fold+file_name+".mp4")
    duration = clip.duration
    nn=0
    batch = 50
    while nn<duration:
        #clip = clip.set_start(nn+1)
        nend = nn+batch
        if nend>duration:
            nend= duration
        clip1 = clip.subclip(nn, nend)
        #clip.audio.write_audiofile(fold+file_name+".mp3")
        #clip.audio.write_audiofile(fold+file_name+".wav", 44100, 2, 2000, "pcm_s32le")
        f_n = fold + file_name+str(nn) + ".wav"
        clip1.audio.write_audiofile(f_n, codec='pcm_s16le')
        nn+=batch
        fileswav.append(f_n)
    return fileswav
    #pcm_s16le
#video2mp3()
#if path.exists(fold+file_name+".mp3"):
#    sound = AudioSegment.from_mp3(file = fold+file_name+".mp3")
#    sound.export(path+file_name+".wav", format="wav")

def mp4_to_wav_mem(file):
    audio = AudioSegment.from_file_using_temporary_files(file, 'mp4')
    file = io.BytesIO()
    file = audio.export(file, format="wav")
    file.seek(0)
    return file

def test():
    fwav = video2mp3()
    r = sr.Recognizer()
    btext = ''
    for fn in fwav:
        print (fn)
        with sr.AudioFile(fn) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            try:
                text = r.recognize_google(audio_data)
            except:
                text = ''
            btext += text
    with open(fold+file_name+".txt", 'w') as infile:
        infile.write(btext)

def speech_to_text(file):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(file)
    with audio as source:
        speech = recognizer.record(source)
        try:
            # Call recognizer with audio and language
            text = recognizer.recognize_google(speech, language='pt-BR')
            print("Você disse: " + text)
            return text
        # If recognizer don't understand
        except:
            print("Não entendi")

def mp4_to_wav(file):
    audio = AudioSegment.from_file(file, format="mp4")
    audio.export("audio.wav", format="wav")
    return audio

def mp4_to_wav_mem(file):
    audio = AudioSegment.from_file_using_temporary_files(file, 'mp4')
    file = io.BytesIO()
    file = audio.export(file, format="wav")
    file.seek(0)
    return file



test()
#f =  open(fold+file_name+".mp4", 'rb')
#file = io.BytesIO(f.read())
#file = mp4_to_wav_mem(file)
#speech_to_text(file)
#f.close()


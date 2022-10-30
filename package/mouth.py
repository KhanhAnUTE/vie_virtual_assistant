from gtts import gTTS
import playsound
import os

language = "vi"

def speak(robot_brain, language=language):
	if robot_brain == "":
		return
	tts = gTTS(text=robot_brain, lang=language, slow=False)
	filedir = "asset/audio/sound.mp3"
	tts.save(filedir)
	print("Robot: " + robot_brain)
	playsound.playsound(filedir)
	os.remove(filedir)

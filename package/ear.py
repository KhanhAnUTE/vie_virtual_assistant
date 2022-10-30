from requests import RequestException
import speech_recognition
import sys

robot_ear = speech_recognition.Recognizer()
language = "vi-VI"

def listen(language=language, silent=False):
	try:
		print(2/0)
		with speech_recognition.Microphone() as mic:
			if not silent:
				print("Candy: Mời bạn nói...")
			robot_ear.adjust_for_ambient_noise(mic, duration=0.2)
			audio = robot_ear.listen(mic, phrase_time_limit=5)

		you = robot_ear.recognize_google(audio, language=language)
	except KeyboardInterrupt:
		sys.exit(0)
	except speech_recognition.RequestError:
		print("Không có kết nối Internet, vui lòng kiểm tra kết nối và thử lại")
		sys.exit(0)
	except:
		you = ""
		you = input('You: ')
	if not silent:
		print("You: " + you)
	return you
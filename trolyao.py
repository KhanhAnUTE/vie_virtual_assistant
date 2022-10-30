from package.ear import listen
from package.brain import think
from package.action import Action

activating = True
silent = False
trolyao = Action()

missing_count = 0
max_missing_count = 3

while activating:
	if not silent:
		ques = listen()
		if ques == '':
			missing_count += 1
			if missing_count >= max_missing_count:
				missing_count = 0
				silent = True
				trolyao.speak("Candy không nhận phản hồi từ bạn, hãy gọi Candy khi cần")
		else:
			missing_count = 0
			ans, tag = think(ques)
			silent = trolyao.act(ans, tag)

			if "bye" == tag:
				activating = False
	else:
		command = listen(silent=silent, language='en')
		command = command.lower()
		if "candy" in command or 'kandi' in command:
			silent = False
			trolyao.speak("Candy vẫn ở đây")
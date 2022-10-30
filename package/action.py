import os
import urllib.request as urllib2
import json
import ctypes
import win32con
import wikipedia
import requests
import webbrowser
from random import randint
from youtube_search import YoutubeSearch
from datetime import datetime
from gtts import gTTS
import playsound
import time
from package.ear import listen

#get user info
with open('asset/data/user_info.json', encoding='utf-8') as f:
    user = json.load(f)

#get stories
with open('asset/data/stories.txt', 'rt', encoding='utf-8') as f:
    stories = f.read()
stories = stories.split('--')

#set up language
language = "vi"
wikipedia.set_lang('vi') 
#save current wallpaper
ubuf = ctypes.create_unicode_buffer(512)
ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER,len(ubuf),ubuf,0)
my_wallpaper = ubuf.value

#store directories that ussually contain win app
current_dir = os.getcwd()
apps_dirs = ["C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\"]
path = os.path.join('C:\\Users\\', os.getlogin(),'Desktop\\')
apps_dirs.append(path)

#boolean
IS_SILENT = True
NOT_SILENT = False

class Action:
    def act(self, ans, tag):
        status = NOT_SILENT
        if tag == "hello":
            status = self.__hello(ans, tag)
        elif tag == "time" or tag == "date":
            status =  self.__get_time(ans, tag)
        elif tag == "weather":
            status =  self.__current_weather(ans, tag)
        elif tag == "wiki":
            status =  self.__tell_me_about(ans, tag)
        elif tag == "playsong":
            status =  self.__play_song(ans, tag)
        elif tag == "open website":
            status =  self.__open_website(ans, tag)
        elif tag == "search google":
            status =  self.__open_google_and_search(ans, tag)
        elif tag == "open app":
            status =  self.__open_application(ans, tag)
        elif tag == "wallpaper":
            status =  self.__change_wallpaper(ans, tag)
        elif tag == 'me':
            status = self.__me(ans, tag)
        elif tag == 'story':
            status = self.__story(ans, tag)
        elif tag == 'sad':
            status = self.__sad(ans, tag)
        else:
            status =  self.__speak(ans, tag)

        return status

    def speak(self, ans):
        self.__speak(ans)

    def __hello(self, ans, tag):
        hour = datetime.now().hour
        if 4 <= hour <= 10:
            ans = 'Chào buổi sáng, ngày mới vui vẻ nha'
        elif 15 < hour <= 18:
            ans = 'Candy xin chào, buổi chiều vui vẻ'
        elif 19 < hour <= 22:
            ans = 'Xin chào buổi tối'
        elif 22 < hour <= 24 or 0 <= hour <= 3:
            ans = 'Candy chào bạn, khuya rồi không nên thức khuya bạn nha'
        if user['name'] != '':
            name = user['name']
            ans = f'Chào {name} nha, thật vui khi gặp lại bạn'
        self.__speak(ans, tag)
        return NOT_SILENT

    def __speak(self, ans, tag='', language='vi'):
        if ans == "":
            return NOT_SILENT
        tts = gTTS(text=ans, lang=language, slow=False)
        filedir = "asset/audio/sound.mp3"
        tts.save(filedir)
        print("Candy: " + ans)
        playsound.playsound(filedir)
        os.remove(filedir)

        return NOT_SILENT

    def __check_acception(self, you):
        accepts = ['okay', 'oke', 'okê', 'có', 'ok', 'được']
        for accept in accepts:
            if accept in you:
                return True
        return False
    def __story(self, ans, tag):
        count = 0
        while True:
            count += 1
            index = randint(0, len(stories) - 1)
            self.__speak(stories[index])
            time.sleep(1)
            if count == 3:
                self.__speak('Candy kể chuyện có làm bạn vui không')
                you = listen()
                if self.__check_acception(you):
                    self.__speak('Candy rất vui khi làm bạn vui')
                else:
                    self.__speak('Candy buồn vì không làm bạn vui được')
                    return NOT_SILENT
            self.__speak('Bạn có muốn nghe tiếp không?')
            you = listen()
            if not self.__check_acception(you):
                self.__speak('Okay nè')
                break
        return NOT_SILENT

    def __sad(self, ans, tag):
        you = ''
        rand = randint(0, 2)
        if rand != 2:
            ans += " Candy đã học hỏi được một vài cách để vượt qua nổi buồn, hãy để Candy giúp bạn."
        if rand == 0:
            self.__speak(ans + ' Bạn có muốn nghe vài bản nhạc không?')
            you = listen()
        elif rand == 1:
            self.__speak(ans + ' Bạn có muốn nghe vài mẫu truyện vui không?')
            you = listen()
        else:
            self.__speak('Bạn hãy luôn lạc quan lên nhé, Candy luôn ở bên bạn')
        
        if self.__check_acception(you):
            if rand == 0:
                return self.__play_song('Ca khúc nhạc buồn tâm trạng', tag)
            elif rand == 1:
                return self.__story(you, tag)
        elif rand != 2:
            self.__speak('Candy hiểu rồi...')
        return NOT_SILENT         

    def __get_time(self, ans, tag):
        now = datetime.now()
        if tag == 'time':
            self.__speak('Bây giờ là %d giờ %d phút' % (now.hour, now.minute))
        elif tag == 'date':
            self.__speak("Hôm nay là ngày %d tháng %d năm %d" % (now.day, now.month, now.year))

        return NOT_SILENT

    def __open_website(self, ans, tag):
        #ans: website address, eg: google.com
        if ans == '':
            self.__speak('Bạn muốn mở website nào?')
            ans = listen()
        if ans == '':
            return IS_SILENT

        url = 'https://www.' + ans
        self.__speak(f"Đang mở {ans}.")
        webbrowser.open(url)

        return IS_SILENT

    def __open_google_and_search(self, ans, tag):
        #ans: noun, keyword, eg: egg, how to play...
        if ans == '':
            self.__speak('Bạn muốn tìm kiếm gì?')
            ans = listen()
        if ans == '':
            return IS_SILENT
        self.__speak(f"Đang tìm kiếm {ans}")
        webbrowser.open("https://www.google.com/search?q=" + ans)

        return IS_SILENT

    def __tell_me_about(self, ans, tag):
        #ans: topic you want assistant to tell you
        try:
            if ans == '':
                self.__speak("Bạn muốn nghe về gì?")
                you = listen()
            contents = wikipedia.summary(you).split('\n')
            count = 0
            self.__speak("Theo wikipedia, ")
            while count < len(contents):
                self.__speak(contents[count])
                if count + 1 < len(contents):
                    self.__speak("Bạn muốn nghe thêm không?")
                    you = listen()
                    if 'có' in you:
                        count += 1
                    else:
                        break
                else:
                    break
            self.__speak('Candy cảm ơn bạn đã lắng nghe!')
        except Exception as e:
            self.__speak("Candy không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại.")
        return NOT_SILENT

    def __play_song(self, ans, tag):
        #ans: name of song
        if ans == '':
            self.__speak('Mời bạn chọn tên bài hát')
            ans = listen()
        if ans == '':
            return IS_SILENT
        self.__speak('Hãy chờ Candy trong giây lát')
        while True:
            result = YoutubeSearch(ans, max_results=10).to_dict()
            if result:
                break
        url = 'https://www.youtube.com' + result[0]['url_suffix']
        self.__speak("Candy đã mở bài hát. Chúc bạn nghe nhạc vui vẻ")
        webbrowser.open(url)

        return IS_SILENT
    
    def __find_app_dir(self, string, directory):
        if string == "":
            return string
        is_finded = False

        #get list of applications in directory
        app_dir = directory
        os.chdir(directory)
        app_list = os.listdir()

        #find app match with string
        for app in app_list:
            if is_finded:
                break
            if '.' in app:
                if string.lower() in app.lower() and '.lnk' in app:
                    app_dir += app
                    is_finded = True
            else:
                temp_dir = app_dir + app + '\\'
                os.chdir(temp_dir)
                temp_list = os.listdir()

                for temp in temp_list:
                    if '.lnk' in temp and string.lower() in temp.lower():
                        temp_dir += temp
                        app_dir = temp_dir
                        is_finded = True
                        break

        #if can't find it
        if is_finded == False:
            app_dir = ''

        os.chdir(current_dir)
        return app_dir
    def __open_application(self, ans, tag):
        #ans: name of your application
        if ans == "":
            self.__speak("Bạn muốn mở ứng dụng nào?")
            ans = listen()
            ans = ans.lower()
        if ans == '':
            return IS_SILENT

        for app_dir in apps_dirs:
            app_dir = self.__find_app_dir(ans, app_dir)
            if app_dir:
                break
        #app_dir is the directory of your application

        if app_dir:
            self.__speak('Candy đang mở ' + ans.title() + ". Chờ Candy trong giây lát nha")
            os.startfile(app_dir)
        else:
            self.__speak('Candy không thể tìm thấy ứng dụng của bạn')
            return NOT_SILENT
        
        return IS_SILENT

    def __change_wallpaper(self, ans, tag):
        api_key = 'RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key
        self.__speak('Okay luôn, chờ Candy xíu nha')
        while True:
            f = urllib2.urlopen(url)
            json_string = f.read()
            f.close()
            parsed_json = json.loads(json_string)
            photo = parsed_json['urls']['full']
            img_dir = os.path.dirname(__file__) + "\\..\\asset\\img\\a.png"
            urllib2.urlretrieve(photo, img_dir)
            image = os.path.join(img_dir)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
            self.__speak('Hình nền máy tính vừa được thay đổi')
            self.__speak('Bạn có muốn đổi tiếp hình nền khác không')
            # you = input('you: ')
            you = listen()
            if "có" in you:
                pass
            elif "cũ" in you or 'của tôi' in you or 'đổi lại' in you:
                image = os.path.join(my_wallpaper)
                ctypes.windll.user32.SystemParametersInfoW(20,0,my_wallpaper,3)
                self.__speak('Hình nền máy tính đã được đưa về như cũ')
                break
            else:
                self.__speak("Đã rõ")
                break
        return NOT_SILENT

    def __current_weather(self, ans, tag):
        #ans: your city
        if ans == '':
            self.__speak("Bạn muốn xem thời tiết ở đâu?")
            # city = input("you: ")
            ans = listen()
        if not ans:
            return IS_SILENT
        ow_url = "http://api.openweathermap.org/data/2.5/weather?"
        api_key = "fe8d8c65cf345889139d8e545f57819a"
        call_url = ow_url + "appid=" + api_key + "&q=" + ans + "&units=metric"
        response = requests.get(call_url)
        data = response.json()
        if data["cod"] != "404":
            city_res = data["main"]
            current_temperature = city_res["temp"]
            current_pressure = city_res["pressure"]
            current_humidity = city_res["humidity"]
            suntime = data["sys"]
            sunrise = datetime.fromtimestamp(suntime["sunrise"])
            sunset = datetime.fromtimestamp(suntime["sunset"])
            wthr = data["weather"]
            weather_description = wthr[0]["description"]
            now = datetime.now()
            content = f"""
            {ans.title()} hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
            Mặt trời mọc vào {sunrise.hour} giờ {sunrise.minute} phút
            Mặt trời lặn vào {sunset.hour} giờ {sunset.minute} phút
            Nhiệt độ trung bình là {current_temperature} độ C
            Áp suất không khí là {current_pressure} Hectopascal
            Độ ẩm là {current_humidity}%
            Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi."""
            self.__speak(content)
            time.sleep(2)
        else:
            self.__speak("Không tìm thấy địa chỉ bạn yêu cầu")

        return NOT_SILENT

    def __me(self, ans, tag):
        name = user['name']
        if name == '':
            self.__speak("Candy chưa biết tên bạn, bạn cho tôi biết được chứ?")
            name = listen()
            self.__speak("Tên bạn là " + name + ". Bạn có muốn tôi gọi bạn là " + name + " không?")
            you = listen()
            if 'có' in you or 'okay' in you or 'được' in you:
                user['name'] = name
                self.__speak('Candy sẽ nhớ tên ' + name)
                with open('asset/data/user_info.json', 'w', encoding='utf-8') as f:
                    json.dump(user, f)
            else:
                self.__speak('Vậy thôi')
        else:
            self.__speak('Candy vẫn nhớ tên bạn là ' + name)

                

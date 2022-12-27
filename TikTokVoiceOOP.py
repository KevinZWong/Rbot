
import requests, base64, random, argparse, os, playsound, time, re, textwrap

# https://twitter.com/scanlime/status/1512598559769702406



class TikTokVoice:

    voices = [
        # DISNEY VOICES
        'en_us_ghostface',            # Ghost Face
        'en_us_chewbacca',            # Chewbacca
        'en_us_c3po',                 # C3PO
        'en_us_stitch',               # Stitch
        'en_us_stormtrooper',         # Stormtrooper
        'en_us_rocket',               # Rocket

        # ENGLISH VOICES
        'en_au_001',                  # English AU - Female
        'en_au_002',                  # English AU - Male
        'en_uk_001',                  # English UK - Male 1
        'en_uk_003',                  # English UK - Male 2
        'en_us_001',                  # English US - Female (Int. 1)
        'en_us_002',                  # English US - Female (Int. 2)
        'en_us_006',                  # English US - Male 1
        'en_us_007',                  # English US - Male 2
        'en_us_009',                  # English US - Male 3
        'en_us_010',                  # English US - Male 4

        # EUROPE VOICES
        'fr_001',                     # French - Male 1
        'fr_002',                     # French - Male 2
        'de_001',                     # German - Female
        'de_002',                     # German - Male
        'es_002',                     # Spanish - Male

        # AMERICA VOICES
        'es_mx_002',                  # Spanish MX - Male
        'br_001',                     # Portuguese BR - Female 1
        'br_003',                     # Portuguese BR - Female 2
        'br_004',                     # Portuguese BR - Female 3
        'br_005',                     # Portuguese BR - Male

        # ASIA VOICES
        'id_001',                     # Indonesian - Female
        'jp_001',                     # Japanese - Female 1
        'jp_003',                     # Japanese - Female 2
        'jp_005',                     # Japanese - Female 3
        'jp_006',                     # Japanese - Male
        'kr_002',                     # Korean - Male 1
        'kr_003',                     # Korean - Female
        'kr_004',                     # Korean - Male 2

        # SINGING VOICES
        'en_female_f08_salut_damour'  # Alto
        'en_male_m03_lobby'           # Tenor
        'en_female_f08_warmy_breeze'  # Warmy Breeze
        'en_male_m03_sunshine_soon'   # Sunshine Soon

        # OTHER
        'en_male_narration'           # narrator
        'en_male_funny'               # wacky
        'en_female_emotional'         # peaceful
    ]

    def __init__(self):
        self.voice = "en_us_010"
        self.text = "Hello World"
        self.session = "0c0991424159487e770cc856fb01d824"
        self.file = None
        self.name = "voice.mp3"
        self.play = False
        #voice, text, session, file, name , play

        '''
        self.voice = input_voice
        self.text = input_text
        self.session = input_session
        self.file = input_file
        self.name = input_name
        self.play = input_play
        '''

    def getVoice(self):
        return self.voice
    def getText(self):
        return self.text
    def getSession(self):
        return self.session
    def getFile(self):
        return self.file
    def getName(self):
        return self.name
    def getPlay(self):
        return self.play

    def setVoice(self, input_voice):
        self.voice = input_voice
    def setText(self, input_text):
        self.text = input_text
    def setSession(self, input_session):
        self.session = input_session
    def setFile(self, input_file):
        self.file = input_file
    def setName(self, input_name):
        self.name = input_name
    def setPlay(self, input_play):
        self.play = input_play



    def tts(self, session_id: str, text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech", filename: str = 'voice.mp3', play: bool = False):

        req_text = req_text.replace("+", "plus")
        req_text = req_text.replace(" ", "+")
        req_text = req_text.replace("&", "and")

        headers = {
            'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
            'Cookie': f'sessionid={session_id}'
        }
        url = f"https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
        r = requests.post(url, headers = headers)

        if r.json()["message"] == "Couldn't load speech. Try again.":
            output_data = {"status": "Session ID is invalid", "status_code": 5}
            print(output_data)
            return output_data

        vstr = [r.json()["data"]["v_str"]][0]
        msg = [r.json()["message"]][0]
        scode = [r.json()["status_code"]][0]
        log = [r.json()["extra"]["log_id"]][0]
        
        dur = [r.json()["data"]["duration"]][0]
        spkr = [r.json()["data"]["speaker"]][0]

        b64d = base64.b64decode(vstr)

        with open(filename, "wb") as out:
            out.write(b64d)

        output_data = {
            "status": msg.capitalize(),
            "status_code": scode,
            "duration": dur,
            "speaker": spkr,
            "log": log
        }

        print(output_data)

        if play is True:
            playsound.playsound(filename)
            os.remove(filename)

        return output_data

    def tts_batch(self, session_id: str, text_speaker: str = 'en_us_002', req_text: str = 'TikTok Text to Speech', filename: str = 'voice.mp3'):
        global voices
        req_text = req_text.replace("+", "plus")
        req_text = req_text.replace(" ", "+")
        req_text = req_text.replace("&", "and")

        headers = {
            'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
            'Cookie': f'sessionid={session_id}'
        }
        url = f"https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"

        r = requests.post(url, headers=headers)

        if r.json()["message"] == "Couldn't load speech. Try again.":
            output_data = {"status": "Session ID is invalid", "status_code": 5}
            print(output_data)
            return output_data

        vstr = [r.json()["data"]["v_str"]][0]
        msg = [r.json()["message"]][0]
        scode = [r.json()["status_code"]][0]
        log = [r.json()["extra"]["log_id"]][0]
        
        dur = [r.json()["data"]["duration"]][0]
        spkr = [r.json()["data"]["speaker"]][0]

        b64d = base64.b64decode(vstr)
        
        with open(filename, "wb") as out:
            out.write(b64d)

        output_data = {
            "status": msg.capitalize(),
            "status_code": scode,
            "duration": dur,
            "speaker": spkr,
            "log": log
        }

        print(output_data)

        return output_data

    def batch_create(filename: str = 'voice.mp3'):
        global voices
        out = open(filename, 'wb')

        def sorted_alphanumeric(data):
            convert = lambda text: int(text) if text.isdigit() else text.lower()
            alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
            return sorted(data, key=alphanum_key)
        
        for item in sorted_alphanumeric(os.listdir('./batch/')):
            filestuff = open('./batch/' + item, 'rb').read()
            out.write(filestuff)

        out.close()

    def GenerateMP3(self):
        
        global voices

        voice = self.voice
        text = self.text
        session = self.session
        file = self.file
        name = self.name
        play = self.play


        '''
        parser = argparse.ArgumentParser(description = "Simple Python script to interact with the TikTok TTS API")
        parser.add_argument("-v", "--voice", help = "the code of the desired voice")
        parser.add_argument("-t", "--text", help = "the text to be read")
        parser.add_argument("-s", "--session", help = "account session id")
        parser.add_argument("-f", "--file", help = "use this if you wanna use 'text.txt'")
        parser.add_argument("-n", "--name", help = "The name for the output file (.mp3)")
        parser.add_argument("-p", "--play", action='store_true', help = "use this if you want to play your output")
        args = parser.parse_args()

        '''



        text_speaker = voice

        if file is not None:
            req_text = open(file, 'r', errors='ignore', encoding='utf-8').read()
        else:
            if text == None:
                req_text = 'TikTok Text To Speech'
                print('You need to have one form of text! (See README.md)')
            else:
                req_text = text

        if play is not None:
            play = play

        if voice == None:
            text_speaker = 'en_us_002'
            print('You need to have a voice! (See README.md)')

        if text_speaker == "random":
            text_speaker = self.randomvoice()

        if name is not None:
            filename = name
        else:
            filename = 'voice.mp3'

        if session is None:
            print('FATAL: You need to have a TikTok session ID!')
            exit(1)

        if file is not None:
            chunk_size = 200
            textlist = textwrap.wrap(req_text, width=chunk_size, break_long_words=True, break_on_hyphens=False)

            os.makedirs('./batch/')

            for i, item in enumerate(textlist):
                self.tts_batch(session, text_speaker, item, f'./batch/{i}.mp3')
            
            self.batch_create(filename)

            for item in os.listdir('./batch/'):
                os.remove('./batch/' + item)
            
            os.removedirs('./batch/')

            return

        self.tts(session, text_speaker, req_text, filename, play)
        


    def randomvoice(self):
        global voices
        count = random.randint(0, len(voices))
        text_speaker = voices[count]

        return text_speaker

    def sampler(self):
        global voices
        for item in voices:
            text_speaker = item
            filename = item
            print(item)
            req_text = 'TikTok Text To Speech Sample'
            self.tts(text_speaker, req_text, filename)

#voice, text, session, file, name , play
'''
TikTokVoice1 = TikTokVoice()
TikTokVoice1.GenerateMP3()

'''






    #python TikTokVoices.py -v en_us_006 -t "hello there" -s 0c0991424159487e770cc856fb01d824 -p
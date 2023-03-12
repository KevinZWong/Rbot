import openai
import re


Script =  ['UPDATE: r/storytime is now a public sub! Make sure to check out our brand new sister sub r/fictiontime', "That's right folks, after four long months I have finally \nbeen able to work on this sub. ", 'No longer will you need to be on an approved \nusers list. ', 'Feel free to post all you want but make sure \nto keep our rules in mind. ', 'Also feel free to check out our brand new sister \nsub r/fictiontime a fun collaborative creative writing subreddit run by \nthe mod team of r/storytime! ', 'Have fun sharing your stories with all you fellow story \ntimers! ']


class YoutubeUpload:
    openai.api_key = "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"
    def __init__(self):
        self.model_engine = "text-davinci-002"
        
    def generateVideoTitle(self, script):
        model_prompt = "Sumarize the following passage into a 1 sentence clickbait title \n\n" + script[0]
        completions = openai.Completion.create(
            engine=self.model_engine,
            prompt=model_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        results = completions.choices[0].text
        results = re.sub('[^0-9a-zA-Z\n\.\?\!]+', ' ', results).strip()
        return results
    def generateVideoDescription(self, script):
        model_prompt = "Sumarize the following,\n\n" + script[0]
        completions = openai.Completion.create(
            engine=self.model_engine,
            prompt=model_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        results = completions.choices[0].text
        results = re.sub('[^0-9a-zA-Z\n\.\?\!]+', ' ', results).strip()
        return results
    def generateVideoTags(self, script):
        pass
    def generateVideoCategories(self, script):
        categories = {
                "Film & Animation": "1",
                "Autos & Vehicles": "2",
                "Music": "10",
                "Pets & Animals": "15",
                "Sports": "17",
                "Short Movies": "18",
                "Travel & Events": "19",
                "Gaming": "20",
                "Videoblogging": "21",
                "People & Blogs": "22",
                "Comedy": "34",
                "Entertainment": "24",
                "News & Politics": "25",
                "Howto & Style": "26",
                "Education": "27",
                "Science & Technology": "28",
                "Nonprofits & Activism": "29",
                "Movies": "30",
                "Anime/Animation": "31",
                "Action/Adventure": "32",
                "Classics": "33",
                "Documentary": "35",
                "Drama": "36",
                "Family": "37",
                "Foreign": "38",
                "Horror": "39",
                "Sci-Fi/Fantasy": "40",
                "Thriller": "41",
                "Shorts": "42",
                "Shows": "43",
                "Trailers": "44"
            }
        return categories["Shorts"]
    def GenerateAll(self, script):
        self.generateVideoTitle(script)
        self.generateVideoDescription(script)
        self.generateVideoTags(script)
        self.generateVideoCategories(script)


if __name__ == "__main__":
    YoutubeUpload1 = YoutubeUpload()
    print(YoutubeUpload1.generateVideoDescription(Script))

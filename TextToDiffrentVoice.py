
import pyttsx3
  

converter = pyttsx3.init()
  

converter.setProperty('rate', 200)
converter.setProperty('volume', 0.7)

converter.say("Trigger warning: blood, injury, throwing up. So, mandatory this happened last Wednesday night. Me and my partner are not good at basic adult stuff like taking the recycling out every week. ")
converter.runAndWait()
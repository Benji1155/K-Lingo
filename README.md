
![K-Lingo](https://i.imgur.com/c3k7XfS.png)

# K-Lingo - Korean made simple.

[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Benji1155/K-Lingo)](https://img.shields.io/github/v/release/Benji1155/K-Lingo)
[![GitHub last commit](https://img.shields.io/github/last-commit/Benji1155/K-Lingo)](https://img.shields.io/github/last-commit/Benji1155/K-Lingo)
[![GitHub issues](https://img.shields.io/github/issues-raw/Benji1155/K-Lingo)](https://img.shields.io/github/issues-raw/Benji1155/K-Lingo)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Benji1155/K-Lingo)](https://img.shields.io/github/issues-pr/Benji1155/K-Lingo)
[![GitHub](https://img.shields.io/github/license/Benji1155/K-Lingo)](https://img.shields.io/github/license/Benji1155/K-Lingo)

**Images**

![K-Longo](https://i.imgur.com/oX3XUsI.png)

**Introduction**

For this assessment, I developed a speech recognition application called K-Lingo. The app is designed as a translation companion for English-speaking travelers visiting countries where a different language is spoken. Currently, the app supports translations from English to Korean, but it can easily be expanded to include other languages. I chose Korean as the target language due to my personal interest in Korea, and my ability to understand basic Korean allows me to validate the translations.

The app’s primary use case is to assist English speakers in Korea, such as helping them order food at a restaurant, though it has many practical applications.

**Process**

The development of the app involved four main steps:

- Capturing the user's sentence in English.
- Converting the audio to text.
- Translating the text to Korean.
- Speaking the Korean translation aloud to the user.

I also integrated these steps into a graphical user interface (GUI) to make the app more user-friendly.
**Step-by-Step Process:**

**Capturing User Input:**
- I set up the microphone to capture the user's speech. A button was used to trigger the listening function, and I configured the microphone to adjust for ambient noise to improve accuracy.

- Converting Audio to Text:
    The microphone input was immediately converted into text. This text was displayed in the app's output window, showing the user what had been captured.

- Translating the Text:
    I used Google Translate’s DeepL translation tool to translate the English text into Korean. This was a free service that did not require API signups. I simply input the sentence and set the target language to Korean. Error handling was implemented to ensure smooth operation.

- Speaking the Translation:
    The translated text was then read aloud to the user using gTTS (Google Text-to-Speech). This provided both visual and auditory options for the user to hear the translation.

Initially, I considered preprocessing the data (e.g., removing stop words or punctuation), but I found that doing so worsened the translation accuracy. It’s important to include all words in the sentence, as removing certain elements can drastically change the meaning.
Conclusion

**In conclusion**, I successfully created a useful application that effectively translates English to Korean. The app features a well-designed GUI, making it easy to use. Although the app could be extended to support Korean to English translations, it currently serves its purpose well and could be expanded to other language pairs in the future.

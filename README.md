# Answer Analysis and Theme Generation
This project analyse text for most common keywords found in a paragraph. This can be a combination of students'
answers as one long paragraph. The python code analyze the data and return defined no of themes consisting of defined no of words in each theme. You can provide stop words that you wish to exclude from the result such as "of", "the", "are" etc. It also generates json data for Arborjs to display the connection between these themes i.e. most common words used between themes and Tag clouds.


## Getting Started

Clone the repo.
Post data to return Themes, Arbor json and Tag Clouds
parameters:
    themeData: json data of answers with answers, questionIDs
    stopwords: json data of stop words
return data in json for Themes, Arbor Js and Tag Clouds

### Prerequisites

- Python 2.7

### Installing

1. Clone the repo
2. Install the dependencies

```
    $ python -m pip install -r requirements.txt
```

3. Run the tests

## Running the tests

```
    cd src/
    python -m tests.test
```

### Break down into end to end tests

Using Python in-built unittest. These test is to check basic functionality of this project

1. Strip tags function - this function should strip any html tags and return text
```
test_clean_html_tags2(self):
    self.assertEqual( remove_html_tags('<table><tr><td>test</td></tr><table>'), 'test')
```

2. find themes function - this function should evaluate words and return common keywords in form of Themes 
```
def test_find_themes(self):
    nothemes = 2
    wordlist = ""
    question_responses = [["The consequence of these differences is that in biology unique historical events can have effects that last for millions of years. Something that happened to one of my ancestors thousands or millions of years ago can still affect me now, because the information about that event has been passed down to me in the genes that I have inherited from that ancestor. There may be no other evidence of that past event except in my genes. No physicist has to deal with this concept — in physics, those past events that have an effect now do so by leaving observable traces in the environment. The laws of physics that operated back then are still operating now, and we can therefore study them now.","","1"],["Magnetic forces separate the charges and cause a potential difference between the ends. This is a motional emf. Conditions required are as follow :　 1）There must exists a magnetic field that is not zero.    2) The conductor must move with the velocity that is no parallel to the magnetic field","","2"]]
    themes = findthemes(nothemes,wordlist,question_responses,STOP_WORDS)
    themesInfo =  json.loads(themes)

    #if no of Themes is 2
    self.assertEqual(themesInfo["themesData"],"Not enough data")
```


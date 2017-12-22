import unittest
import sys
import platform
import json
#sys.path.insert(0, 'C:\\Bitnami\\wampstack-5.6.31-0\\apache2\\htdocs\\answer-analysis\\src\\nnmf')
from nnmf.default import remove_html_tags, findthemes

STOP_WORDS  = ["-","a","a's","able","about","above","abroad","according","accordingly","across","actually","adj","after","afterwards","again","against","ago","ahead","ain't","all","allow","allows","almost","alone","along","alongside","already","also","although","always","am","amid","amidst","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","b","back","backward","backwards","be","became","because","become","becomes","becoming","been","before","beforehand","begin","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","c'mon","c's","came","can","can't","cannot","cant","caption","cause","causes","certain","certainly","changes","clearly","co","co.","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","d","dare","daren't","definitely","described","despite","did","didn't","different","directly","do","does","doesn't","doing","don't","done","down","downwards","during","e","each","edu","eg","eight","eighty","either","else","elsewhere","end","ending","enough","entirely","especially","et","etc","even","ever","evermore","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","fairly","far","farther","few","fewer","fifth","first","five","followed","following","follows","for","forever","former","formerly","forth","forward","found","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","half","happens","hardly","has","hasn't","have","haven't","having","he","he'd","he'll","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","hundred","i","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","inc.","indeed","indicate","indicated","indicates","inner","inside","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","j","just","k","keep","keeps","kept","know","known","knows","l","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","likewise","little","look","looking","looks","low","lower","lsquo","ltd","m","made","mainly","make","makes","many","may","maybe","mayn't","me","mean","meantime","meanwhile","merely","might","mightn't","mine","minus","miss","more","moreover","most","mostly","mr","mrs","much","must","mustn't","my","myself","n","name","namely","nbsp","nd","near","nearly","necessary","need","needn't","needs","neither","never","neverf","neverless","nevertheless","new","next","nine","ninety","no","no-one","nobody","non","none","nonetheless","noone","nor","normally","not","nothing","notwithstanding","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","one's","ones","only","onto","opposite","or","other","others","otherwise","ought","oughtn't","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","past","per","perhaps","placed","please","plus","possible","presumably","probably","provided","provides","q","que","quite","quot","qv","r","rather","rd","re","really","reasonably","recent","recently","regarding","regardless","regards","relatively","respectively","right","round","rsquo","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","shan't","she","she'd","she'll","she's","should","shouldn't","since","six","so","some","somebody","someday","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t",  "t's","take","taken","taking","tell","tends","th","than","thank","thanks","thanx","that","that'll","that's","that've","thats","the","their","theirs","them","themselves","then","thence","there","there'd","there'll","there're","there's","there've","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","thing","things","think","third","thirty","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","till","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","u","un","under","underneath","undoing","unfortunately","unless","unlike","unlikely","until","unto","up","upon","upwards","us","use","used","useful","uses","using","usually","v","value","various","versus","very","via","viz","vs","w","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what'll","what's","what've","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","whichever","while","whilst","whither","who","who'd","who'll","who's","whoever","whole","whom","whomever","whose","why","will","willing","wish","with","within","without","won't","wonder","would","wouldn't","x","y","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","z","zero"]

class TestStringMethods(unittest.TestCase):

  

    def test_clean_html_tags(self):
        self.assertEqual( remove_html_tags('<p>test</p>'), 'test')   
    
    def test_clean_html_tags2(self):
        self.assertEqual( remove_html_tags('<table><tr><td>test</td></tr><table>'), 'test')

    def test_clean_html_tags3(self):
        self.assertEqual( remove_html_tags('<p>I</p><table><tr><td>run</td></tr><table><strong>fast</strong>'), 'Irunfast')
        
    def test_find_themes(self):
        nothemes = 4
        wordlist = ""
        question_responses = [["The consequence of these differences is that in biology unique historical events can have effects that last for millions of years. Something that happened to one of my ancestors thousands or millions of years ago can still affect me now, because the information about that event has been passed down to me in the genes that I have inherited from that ancestor. There may be no other evidence of that past event except in my genes. No physicist has to deal with this concept — in physics, those past events that have an effect now do so by leaving observable traces in the environment. The laws of physics that operated back then are still operating now, and we can therefore study them now.","","1"],["Magnetic forces separate the charges and cause a potential difference between the ends. This is a motional emf. Conditions required are as follow :　 1）There must exists a magnetic field that is not zero.    2) The conductor must move with the velocity that is no parallel to the magnetic field","","2"]]
        themes = findthemes(nothemes,wordlist,question_responses,STOP_WORDS)
        themesInfo =  json.loads(themes)
        
        #if no of Themes is 2
        self.assertEqual(themesInfo["themesData"],"Not enough data")

    def test_find_theme_first_word(self):
        nothemes = 1
        wordlist = ""
        question_responses = [["The consequence of these differences is that in biology unique historical events can have effects that last for millions of years. Something that happened to one of my ancestors thousands or millions of years ago can still affect me now, because the information about that event has been passed down to me in the genes that I have inherited from that ancestor. There may be no other evidence of that past event except in my genes. No physicist has to deal with this concept — in physics, those past events that have an effect now do so by leaving observable traces in the environment. The laws of physics that operated back then are still operating now, and we can therefore study them now.","","1"],["Magnetic forces separate the charges and cause a potential difference between the ends. This is a motional emf. Conditions required are as follow :　 1）There must exists a magnetic field that is not zero.    2) The conductor must move with the velocity that is no parallel to the magnetic field","","2"]]
        themes = findthemes(nothemes,wordlist,question_responses,STOP_WORDS)
        themesInfo =  json.loads(themes)
     
        #if no of Themes is 1
        self.assertEqual(themesInfo["themesData"]["Theme1"]["words"]["word1"]['word'],"event")


    def test_return_three_themes(self):
        nothemes = 5
        wordlist = ""
        question_responses = [["Purple","","347527"],["Lilac.","","347529"],["I+believe+that+they+are+purple","","347531"],["Lilac","","347533"],["","","347535"],["Purple","","347537"],["Purple","","347539"],["Light+Purple","","347541"],["Lilac","","347543"],["Lilac","","347545"],["Purple","","347547"],["Light+purple","","347549"],["Purple.","","347551"],["Lilac\/purple","","347553"],["Purple.","","347555"]]
        themes = findthemes(nothemes,wordlist,question_responses,STOP_WORDS)
        themesInfo =  json.loads(themes)

        #return true if it matches with defined no of themes
        self.assertTrue(len(themesInfo["themesData"]),nothemes)
        






if __name__ == '__main__':
    unittest.main()
    
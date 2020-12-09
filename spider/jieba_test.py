import jieba
# from snownlp import SnowNLP
# from snownlp import sentiment
from cnsenti import Emotion
from cnsenti import Sentiment

senti = Sentiment()
emotion = Emotion()
test_text = '来得时-甘精胰岛素说明书'
print(jieba.lcut(test_text))
result = emotion.emotion_count(test_text)
result_o = senti.sentiment_count(test_text)
print(result)
print(result_o)
print(senti.sentiment_calculate(test_text))
# print(result['好'])
import pathlib
import pickle
def read_dict(file):
    pathchain = ['dictionary', 'dutir', file]
    mood_dict_filepath = pathlib.Path(__file__).parent.joinpath(*pathchain)
    dict_f = open(mood_dict_filepath, 'rb')
    words = pickle.load(dict_f)
    return words
print(read_dict('C:/Users\Thinkpad\Anaconda3\Lib\site-packages\cnsenti\dictionary\dutir\惧.pkl'))
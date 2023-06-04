import streamlit as st
import pandas as pd
import random
import speech_recognition as sr
import pyttsx3
import time
import eng_to_ipa as ipa
import pickle as pkl

import time

model = pkl.load(open("model.pkl", 'rb'))

st.set_page_config(page_title="LexiScan", page_icon="🧊", layout="wide", initial_sidebar_state="expanded")


hide_menu_style = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden; }
</style>
"""


st.markdown(hide_menu_style, unsafe_allow_html=True)
st.header("LexiScan - Dyslexia Diagnosis")
st.write("")


#'''-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

def get_10_word_array(level: int):
    if (level == 1):
        voc = pd.read_csv("data/text/intermediate_voc.csv")
        arr = voc.squeeze().to_numpy()
        selected_list = random.sample(list(arr), 10)
        return selected_list
    elif(level == 2):
        voc = pd.read_csv("data/text/elementary_voc.csv")
        # return (type(voc))
        arr = voc.squeeze().to_numpy()
        selected_list = random.sample(list(arr), 10) 
        return selected_list
    else:
        return ([])
    
#'''-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
    
def listen_for(seconds: int):
    with sr.Microphone() as source:
        r = sr.Recognizer()
        print("Recognizing...")
        audio_data = r.record(source, seconds)
        text = r.recognize_google(audio_data)
        print(text)
        return text

 #'''-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
    
def talk(Word : str):
    engine = pyttsx3.init()
    engine.say(Word)
    engine.runAndWait()

#''-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]
#''-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
def check_pronounciation(str1 : str , str2: str):
        s1 = ipa.convert(str1)
        s2 = ipa.convert(str2)
        return levenshtein(s1,s2)

#'''-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
    
def dictate_10_words(level : int):
    words = get_10_word_array(level)
    for i in words:
        talk(i)
        time.sleep(8)
    return words

#'''-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

def random_seq():
    list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']
    return " ".join(random.sample(list, 5))

#'''-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''



#'''-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

tab1, tab2, tab3 = st.tabs(["Home", "pronounciation test", "phonetics"])

level = 1


with tab1:
    st.title("A Test for Dyslexia")
    option = st.selectbox(
        "Select Difficulty", ('Begineer', 'Intermediate'), key= "pro")
    if option=='Begineer':
        level = 2
    elif option == 'Intermediate':
        level = 1

with tab2:
    st.header("The pronounciation and reading ability of the user will be measured here")
    pronounciation_test = st.button("Start a pronouncation test")
    pronounciation_inaccuracy = 0
    
    if pronounciation_test:
        st.subheader("Please repeate the following words you only has 10 seconds to do that.")
        
        arr = get_10_word_array(level)
        for i in range(len(arr)):
            arr[i] = str(arr[i])
            arr[i] = arr[i].strip()
        str_displayed = str(" ".join(arr))
        words = st.text(">> " + "\n>>".join(arr) )
        status = st.text("listenning........")
        str_pronounced = listen_for(10)
        status.write("Time up! calculating inacuracy......")
        
        
        pronounciation_inaccuracy = check_pronounciation(str_displayed, str_pronounced)/len(str_displayed)
        
        words.write("The Pronounciation inacuuracy is: " + str(pronounciation_inaccuracy))
        status.write("Original : " + ipa.convert(str_displayed) )
        st.write("\nPronounced: " + ipa.convert(str_pronounced))
            
with tab3:
    st.subheader("Phonetics")
    st.write("""
                 Phonetics is a branch of linguistics that studies how humans produce and perceive sounds, or in the case of sign languages, the equivalent aspects of sign. 
Phoneticians—linguists who specialize in studying Phonetics the physical properties of speech. When you open any English dictionary, you will find some kind of signs 
after the word, just before the meaning of the word, those signs are called Phonetics. Phonetics will help you, how to pronounce a particular word correctly. It 
gives the correct pronunciation of a word both in British and American English. Phonetics is based on sound.

Learning the basics of phonetics is very simple. The first or the second page of every dictionary will have an index of phonetics. If, you know to read them. That 
is more than enough to help pronounce any word correctly.
Once you know to use phonetics, then you don't have to go behind anybody asking them to help you, to pronounce a particular word. You can do it yourself; 
you can even teach others and correct them when they do not pronounce a word correctly.

Almost all people with dyslexia, however, struggle with spelling and face serious obstacles in learning to cope with this aspect of their learning disability. 
The definition of dyslexia notes that individuals with dyslexia have "conspicuous problems" with spelling and writing, in spite of being capable in other areas 
and having a normal amount of classroom instruction. Many individuals with dyslexia learn to read fairly well, but difficulties with spelling (and handwriting) 
tend to persist throughout life, requiring instruction, accommodations, task modifications, and understanding from those who teach or work with the individual.
                 
                 """)
    st.subheader("What Causes Spelling Mistakes:")
    st.write("""
                 One common but mistaken belief is that spelling problems stem from a poor visual memory for the sequences of letters in words. Recent research, however, shows 
that a general kind of visual memory plays a relatively minor role in learning to spell. Spelling problems, like reading problems, originate with language 
learning weaknesses. Therefore, spelling reversals of easily confused letters such as b and d, or sequences of letters, such as wnet for went are manifestations 
of underlying language learning weaknesses rather than of a visually based problem. Most of us know individuals who have excellent visual memories for pictures, 
color schemes, design elements, mechanical drawings, maps, and landscape features, for example, but who spell poorly. The kind of visual memory necessary for spelling 
is closely "wired in" to the language processing networks in the brain.

Poor spellers have trouble remembering the letters in words because they have trouble noticing, remembering, and recalling the features of language that those letters 
represent. Most commonly, poor spellers have weaknesses in underlying language skills including the ability to analyze and remember the individual sounds (phonemes) 
in the words, such as the sounds associated with j , ch, or v, the syllables, such as la, mem, pos and the meaningful parts (morphemes) of longer words, such as sub-, 
-pect, or -able. These weaknesses may be detected in the use of both spoken language and written language; thus, these weaknesses may be detected when someone speaks and writes.

Like other aspects of dyslexia and reading achievement, spelling ability is influenced by inherited traits. It is true that some of us were born to be better spellers 
than others, but it is also true that poor spellers can be helped with good instruction and accommodations.
Dyslexic people usually spell according to their ability to correctly pronounce words phonetically, but they may not know how to spell some words. For example, 
in ‘phonics’, they could misspell ‘Finnish’. Dyslexics often experience: difficulty reading, such as reading without reading aloud, in teens and adults. Labor-intensive 
reading and writing that is slow and gradual. Spelling problems. Those with dyslexia may be unable to pronounce words with complete accuracy or write in ways they are 
comfortable in any other part of the body other than at school, yet they have “conspicuous difficulties” with both of these parts. Spelling seems to be a challenge that 
persists as a result of dyslexia, but learning how to read with the right support can improve your performance significantly. It has yet to be determined why this is. 
Several studies show that learning difficulties lead to a significant underestimation of phonological processing and memory.
                 """)
        

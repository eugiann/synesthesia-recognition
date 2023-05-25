# -*- coding: utf-8 -*-
"""synesthesia_recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gtPNnQ85GRFrrNjVV80-H1SRCi71BAsm
"""

# 0) Importazione librerie

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize
import pandas as pd


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# 1) Read file and create list of sentences

# split di ukWak pari al 10% del totale (dimensione file 1 GB circa)
eng_corpus = "/content/drive/MyDrive/eng_corpus_ukWac2.txt"  
sentences = []

with open(eng_corpus, encoding = "ISO-8859-1") as file:
  count = sum(1 for _ in file)
  
with open(eng_corpus, encoding = "ISO-8859-1") as file:
  for i, line in enumerate(file):
    if (i%2 !=0):  # salta le righe dispari che contengono i link alle frasi
      continue
    if (i<=count):
      for l in sent_tokenize(line):
        sentences.append(l)
    else:
      break

print(type(sentences))
print(len(sentences))
print(sentences[:10])

# 2) Reading Sensicon 1.0.0 dictionary

sensicon_path='/content/drive/MyDrive/Sensicon/sensicon1.0.0/Sensicon1.0.0.txt'
sensicon = pd.read_csv(sensicon_path, sep='\t', header=None)
sensicon.columns= ['lemma', 'Sight', 'Hearing', 'Taste', 'Smell', 'Touch']
lemmas = [x.split('__') for x in sensicon['lemma'].values]
sensicon['pos'] = [lemma[1] for lemma in lemmas]
sensicon['lemma'] = [lemma[0] for lemma in lemmas]

# 3) Class SensiconWord definition

class SensiconWord:
  def __init__(self, lemma, sight, hearing, taste, smell, touch, is_relevant, pos, position):
    self.lemma=lemma
    self.sight=sight
    self.hearing=hearing
    self.taste=taste
    self.smell=smell
    self.touch=touch
    self.is_relevant=is_relevant
    self.pos=pos
    self.position=position


# 4) Create list of SensiconWord objects (one for each word in the dictionary)

sensicon_word_list = []
with open(sensicon_path) as file1:
    lines = file1.readlines()
    for index, line in enumerate(lines):
       wlist = line.split();
       s = SensiconWord(wlist[0].split('__')[0], wlist[1], wlist[2], 
                        wlist[3], wlist[4], wlist[5], False, wlist[0].split('__')[1], 0)
       sensicon_word_list.append(s)    

print(len(sensicon_word_list))

# 5) Create and populate dictionaries (one for each POS, to avoid duplicates) for nouns (n), adjectives (a), verbs (v) and adverbs (r)
import json

sense_dictionary_nouns = {}
sense_dictionary_adjs = {}
sense_dictionary_verbs = {}
sense_dictionary_advs = {}

for i,s in enumerate(sensicon_word_list):
  if sensicon_word_list[i].pos == 'n':
    sense_dictionary_nouns[s.lemma] = {}
    sense_dictionary_nouns[s.lemma]['sight'] = sensicon_word_list[i].sight
    sense_dictionary_nouns[s.lemma]['hearing'] = sensicon_word_list[i].hearing
    sense_dictionary_nouns[s.lemma]['taste'] = sensicon_word_list[i].taste
    sense_dictionary_nouns[s.lemma]['smell'] = sensicon_word_list[i].smell
    sense_dictionary_nouns[s.lemma]['touch'] = sensicon_word_list[i].touch
  elif sensicon_word_list[i].pos == 'a':
    sense_dictionary_adjs[s.lemma] = {}
    sense_dictionary_adjs[s.lemma]['sight'] = sensicon_word_list[i].sight
    sense_dictionary_adjs[s.lemma]['hearing'] = sensicon_word_list[i].hearing
    sense_dictionary_adjs[s.lemma]['taste'] = sensicon_word_list[i].taste
    sense_dictionary_adjs[s.lemma]['smell'] = sensicon_word_list[i].smell
    sense_dictionary_adjs[s.lemma]['touch'] = sensicon_word_list[i].touch
  elif sensicon_word_list[i].pos == 'v':
    sense_dictionary_verbs[s.lemma] = {}
    sense_dictionary_verbs[s.lemma]['sight'] = sensicon_word_list[i].sight
    sense_dictionary_verbs[s.lemma]['hearing'] = sensicon_word_list[i].hearing
    sense_dictionary_verbs[s.lemma]['taste'] = sensicon_word_list[i].taste
    sense_dictionary_verbs[s.lemma]['smell'] = sensicon_word_list[i].smell
    sense_dictionary_verbs[s.lemma]['touch'] = sensicon_word_list[i].touch
  elif sensicon_word_list[i].pos == 'r':
    sense_dictionary_advs[s.lemma] = {}
    sense_dictionary_advs[s.lemma]['sight'] = sensicon_word_list[i].sight
    sense_dictionary_advs[s.lemma]['hearing'] = sensicon_word_list[i].hearing
    sense_dictionary_advs[s.lemma]['taste'] = sensicon_word_list[i].taste
    sense_dictionary_advs[s.lemma]['smell'] = sensicon_word_list[i].smell
    sense_dictionary_advs[s.lemma]['touch'] = sensicon_word_list[i].touch
 
print(len(sense_dictionary_nouns)) #11083
print(len(sense_dictionary_adjs)) #6721
print(len(sense_dictionary_verbs)) #3738
print(len(sense_dictionary_advs)) #1142
#print(json.dumps(sense_dictionary_advs, indent=4))

# 6) Functions to check if a sentence could contain sinesthesia 

threshold = 0.05

def is_sight_lexeme(token, dictionary):
    dictionary = dictionary.get(token.strip(), {})
    if not bool(dictionary):
       return False
    if float(dictionary.get('sight')) > threshold:
       return True
    else:
       return False

# function to check if a token is a hearing lexeme
def is_hearing_lexeme(token, dictionary):
    dictionary = dictionary.get(token.strip(), {})
    if not bool(dictionary):
       return False
    if float(dictionary.get('hearing')) > threshold: 
       return True
    else:
       return False

def is_smell_lexeme(token, dictionary):
    dictionary = dictionary.get(token.strip(), {})
    if not bool(dictionary):
       return False
    if float(dictionary.get('smell')) > threshold: 
       return True
    else:
       return False

def is_touch_lexeme(token, dictionary):
    dictionary = dictionary.get(token.strip(), {})
    if not bool(dictionary):
       return False
    if float(dictionary.get('touch')) > threshold: 
       return True
    else:
       return False

def is_taste_lexeme(token, dictionary):
    dictionary = dictionary.get(token.strip(), {})
    if not bool(dictionary):
       return False
    if float(dictionary.get('taste')) > threshold: 
       return True
    else:
       return False

# function to check if a sentence contains lexemes from both modalities
def check_sentence(sentence, log):
    sight_found = False
    hearing_found = False
    smell_found = False
    taste_found = False
    touch_found = False
    for tagged_token in nltk.pos_tag(nltk.word_tokenize(sentence)):
      #if log: print(tagged_token)
      word, pos = tagged_token[0], tagged_token[1]
      if pos.startswith('N'):
          if log: print("Word: " + word + ". POS: " + pos)
          if is_sight_lexeme(word, sense_dictionary_nouns): sight_found = True
          if is_hearing_lexeme(word, sense_dictionary_nouns): hearing_found = True
          if is_touch_lexeme(word, sense_dictionary_nouns): touch_found = True
          if is_taste_lexeme(word, sense_dictionary_nouns): taste_found = True
          if is_smell_lexeme(word, sense_dictionary_nouns): smell_found = True
      elif pos.startswith('J'):
          if log: print("Word: " + word + ". POS: " + pos)
          if is_sight_lexeme(word, sense_dictionary_adjs): sight_found = True
          if is_hearing_lexeme(word, sense_dictionary_adjs): hearing_found = True
          if is_touch_lexeme(word, sense_dictionary_adjs): touch_found = True
          if is_taste_lexeme(word, sense_dictionary_adjs): taste_found = True
          if is_smell_lexeme(word, sense_dictionary_adjs): smell_found = True
      elif pos.startswith('V'):
          if log: print("Word: " + word + ". POS: " + pos)
          if is_sight_lexeme(word, sense_dictionary_verbs): sight_found = True
          if is_hearing_lexeme(word, sense_dictionary_verbs): hearing_found = True
          if is_touch_lexeme(word, sense_dictionary_verbs): touch_found = True
          if is_taste_lexeme(word, sense_dictionary_verbs): taste_found = True
          if is_smell_lexeme(word, sense_dictionary_verbs): smell_found = True
      elif pos.startswith('R'):
          if log: print("Word: " + word + ". POS: " + pos)
          if is_sight_lexeme(word, sense_dictionary_advs): sight_found = True
          if is_hearing_lexeme(word, sense_dictionary_advs): hearing_found = True
          if is_touch_lexeme(word, sense_dictionary_advs): touch_found = True
          if is_taste_lexeme(word, sense_dictionary_advs): taste_found = True
          if is_smell_lexeme(word, sense_dictionary_advs): smell_found = True
    return is_sentence_relevant(sight_found, hearing_found, touch_found, taste_found, smell_found)


def is_sentence_relevant(sight_found, hearing_found, touch_found, taste_found, smell_found):
  res = False
  if (sight_found and hearing_found) or (sight_found and touch_found) or (sight_found and taste_found) or (sight_found and smell_found): 
    res = True
  if (hearing_found and touch_found) or (hearing_found and taste_found) or (hearing_found and smell_found): 
    res = True
  if (touch_found and taste_found) or (touch_found and smell_found):
    res = True
  if (taste_found and smell_found):
    res = True
  return res;


def sense_related_lexemes_from_sentence(sentence, log):
   sense_lexemes = []
   position=1
   for tagged_token in nltk.pos_tag(nltk.word_tokenize(sentence)):
     word = tagged_token[0]
     pos = tagged_token[1]
     if log: print(str(position) + " " +pos)
     s = SensiconWord(word, 0.0, 0.0, 0.0, 0.0, 0.0, False, pos, position)
     position+=1;          #lemma, sight, hearing, taste, smell, touch, is_relevant, pos
     if pos.startswith('N'):
        check_sense_related_word(word, sense_dictionary_nouns, s)
     elif pos.startswith('J'):
        check_sense_related_word(word, sense_dictionary_adjs, s)
     elif pos.startswith('V'):
        check_sense_related_word(word, sense_dictionary_verbs, s)  
     elif pos.startswith('R'):
        check_sense_related_word(word, sense_dictionary_advs, s)
     sense_lexemes.append(s)
   return sense_lexemes


def check_sense_related_word(word, dictionary, sensicon_word):
   d = dictionary.get(word.strip(), {})
   if is_hearing_lexeme(word, dictionary): 
     sensicon_word.hearing = float(d.get('hearing'))
     sensicon_word.is_relevant = True
   if is_touch_lexeme(word, dictionary): 
     sensicon_word.touch = float(d.get('touch'))
     sensicon_word.is_relevant = True
   if is_smell_lexeme(word, dictionary): 
     sensicon_word.smell = float(d.get('smell'))
     sensicon_word.is_relevant = True
   if is_sight_lexeme(word, dictionary): 
     sensicon_word.sight = float(d.get('sight'))
     sensicon_word.is_relevant = True
   if is_taste_lexeme(word, dictionary): 
     sensicon_word.taste = float(d.get('taste'))
     sensicon_word.is_relevant = True

def check_if_word_is_in_sensicon(word):
  is_present = False
  for s in sensicon_word_list:
    if s.lemma == word: is_present = True
  return is_present

#def relevant_words_from_sentence()

# 7) Test check sentence function

nltk.download('averaged_perceptron_tagger')
sentence="If you smell a burning smell it usually means the belt if off the spinner."
print("SENTENCE:")
print(sentence+"\n")
print("POS Tagging:")
#print(check_sentence("the silence that dwells in the forest is not so black", True))
print(check_sentence("The opportunity to see and hear the music of these legendary American stars is a rare one, and not an event that should be missed lightly.", True))
# print(check_sentence("the silence that dwells in the forest is not so black", True))
# print(is_sight_lexeme("mauve", sense_dictionary_nouns))
# print(is_hearing_lexeme("sound", sense_dictionary_verbs))
#print(sentences[:10])
#print(sense_related_lexemes_from_sentence(sentence))

# 8) Extract relevant sentences from corpus

relevant_sentences = [sentence for sentence in sentences[:10000] if check_sentence(sentence, False)]
non_relevant_sentences = [sentence for sentence in sentences[:10000] if not check_sentence(sentence, False)]
print(len(relevant_sentences))  #255
print(len(non_relevant_sentences))  #9745

# 9) Verified metaphors from  excel

import json
sinestesie_UKWAC_path='/content/drive/MyDrive/sinestesie_UKWAC_2.xlsx'
sinestesie_UKWAC = pd.read_excel(sinestesie_UKWAC_path, sheet_name='Foglio3')
sinestesie_UKWAC.columns= ['sentence', 'source_s', 'target_s', 'dependency_type', 'syntax', 'source_w', 'target_w', 'comment', 'corpus']

sinestesie_UKWAC_list = []
for i, s in enumerate(sinestesie_UKWAC['sentence']):
  sinestesie_UKWAC_list.append(s[7:])

output = {}
true_counter=0
false_counter=0
for i in range(len(sinestesie_UKWAC_list)):
  if check_sentence(sinestesie_UKWAC_list[i], False):
    print("TRUE " + sinestesie_UKWAC_list[i])
    output[i] = {}
    output[i]['sentence'] = sinestesie_UKWAC_list[i]
    output[i]['relevant'] = True
    true_counter+=1
  else:
    print("FALSE " + sinestesie_UKWAC_list[i])
    output[i] = {}
    output[i]['sentence'] = sinestesie_UKWAC_list[i]
    output[i]['relevant'] = False
    false_counter+=1

#print(json.dumps(output, indent=4))
print(true_counter)
print(false_counter)

#10) Test if a sentence is recognized as relevant correctly

for i, sentence in enumerate(sinestesie_UKWAC_list):
  list_sensic = sense_related_lexemes_from_sentence(sentence, False)
  print(str(i+1) + ") "+ sentence)
  print("Verified synesthetic metaphor:")
  print("Source word: " + sinestesie_UKWAC['source_w'][i], "(" + sinestesie_UKWAC['source_s'][i] +")")
  print("Target word: " + sinestesie_UKWAC['target_w'][i], "(" + sinestesie_UKWAC['target_s'][i] +")")
  print("Syntax: " + sinestesie_UKWAC['syntax'][i])
  print("Dependency type: " + sinestesie_UKWAC['dependency_type'][i])
  
  print("\nSensicon analysis. Relevant words for sentence " + str(i+1))
  for s in list_sensic:
    if s.is_relevant:
      print("(at position " + str(s.position) +")", s.lemma, s.pos, 
            "Vision (" + str(s.sight) + ")" if (s.sight !=0) else "", 
            "Hearing (" + str(s.hearing) + ")" if (s.hearing !=0) else "", 
            "Taste (" +str(s.taste) + ")" if (s.taste !=0) else "", 
            "Smell (" + str(s.smell) + ")" if (s.smell !=0) else "", 
            "Touch (" + str(s.touch) + ")" if (s.touch !=0) else "")
  print("\n")

#11) POS tagging test

#sense_related_lexemes_from_sentence("The songs are wonderful, both awkward and hilarious, and Dan 's voice is something else, so low and warm.", True)

nltk.pos_tag(nltk.word_tokenize("The songs are wonderful, both awkward and hilarious, and Dan 's voice is something else, so low and warm."))
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .nounspider import NounSpider
from django.http import JsonResponse
from django.core.management import call_command
import subprocess
from scrapy.http import TextResponse
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import re

@api_view(['GET'])
def getData(request, query):
  try:
    fetch = "scrapy fetch https://api.verbix.com/conjugator/iv1/6153a464-b4f0-11ed-9ece-ee3761609078/1/75/175/{}".format(query)
    result = subprocess.check_output(fetch, shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
    selector = scrapy.Selector(text=result)
    html = selector.css('html body p div').get()

    # verbs
    if html is not None:
      match = parseTerms(html) if html is not None else {}
      return Response(match)
    # nouns
    else: 
      fetch = "scrapy fetch https://api.verbix.com/conjugator/iv1/6153a464-b4f0-11ed-9ece-ee3761609078/1/1075/1075/{}".format(query)
      result = subprocess.check_output(fetch, shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
      selector = scrapy.Selector(text=result)
      html = selector.css('html body p div').get()
      match = parseTerms2(html) if html is not None else {}
      return Response(match)

  except subprocess.CalledProcessError as e:
    # Handle errors if the command fails
    error_message = f"Error executing command: {e.output}"
    print(error_message)
    return Response({"error": error_message}, status=500)
  

def parseTerms(htmlContent):
  # print("html:", htmlContent)
  normalClass = re.compile(r"(<span class='\\\"normal\\\"'>|<span class='\\\"irregular\\\"'>)(.*?)<\/span>")
  nominalForms = normalClass.findall(htmlContent)
  print(nominalForms)
  infinitive = { 
    "form": nominalForms[0][1], 
    "conjugationType": "normal" if "normal" in nominalForms[0][0] else "irregular"
  }
  pastparticiple = {
    "form": nominalForms[1][1], 
    "conjugationType": "normal" if "normal" in nominalForms[0][0] else "irregular"
  }
  presentParticiple = {
    "form": nominalForms[2][1],
     "conjugationType": "normal" if "normal" in nominalForms[0][0] else "irregular"
  }
  singularImperative = {
    "form": nominalForms[3][1],
    "conjugationType": "normal" if "normal" in nominalForms[3][0] else "irregular"
  }
  pluralImperative = {
    "form": nominalForms[5][1],
    "conjugationType": "normal" if "normal" in nominalForms[5][0] else "irregular"
  }

  columnsSub = re.compile(r"(?<=$<table class='\\\"verbtense\\\"'>).|\n*?(?<=<span data-speech='\\\").*?(?=<\/span>)")
  tensesList = columnsSub.findall(htmlContent)
  presentTenses = extractPresent(tensesList)
  # print(presentTenses)
  firstPersonPresent = {
    "form": presentTenses[0][0],
     "conjugationType": "regular" if "regular" in presentTenses[0][1] else "irregular"
  }
  secondPersonPresent = {
    "form": presentTenses[1][0],
     "conjugationType": "regular" if "regular" in presentTenses[1][1] else "irregular"
  }
  thirdPersonPresent = {
    "form": presentTenses[2][0],
     "conjugationType": "regular" if "regular" in presentTenses[2][1] else "irregular"
  }
  firstPersonPluralPresent = {
    "form": presentTenses[3][0],
     "conjugationType": "regular" if "regular" in presentTenses[3][1] else "irregular"
  }
  secondPersonPluralPresent = {
    "form": presentTenses[4][0],
     "conjugationType": "regular" if "regular" in presentTenses[4][1] else "irregular"
  }
  thirdPersonPluralPresent = {
    "form": presentTenses[5][0],
     "conjugationType": "regular" if "regular" in presentTenses[5][1] else "irregular"
  }
  firstPersonPast = {
    "form": presentTenses[6][0],
     "conjugationType": "regular" if "regular" in presentTenses[6][1] else "irregular"
  }
  secondPersonPast = {
    "form": presentTenses[7][0],
     "conjugationType": "regular" if "regular" in presentTenses[7][1] else "irregular"
  }
  thirdPersonPast = {
    "form": presentTenses[8][0],
     "conjugationType": "regular" if "regular" in presentTenses[8][1] else "irregular"
  }
  firstPersonPluralPast = {
    "form": presentTenses[9][0],
     "conjugationType": "regular" if "regular" in presentTenses[9][1] else "irregular"
  }
  secondPersonPluralPast = {
    "form": presentTenses[10][0],
     "conjugationType": "regular" if "regular" in presentTenses[10][1] else "irregular"
  }
  thirdPersonPluralPast = {
    "form": presentTenses[11][0],
     "conjugationType": "regular" if "regular" in presentTenses[11][1] else "irregular"
  }

  # print(presentTenses)
  
  return {
    "infinitive": infinitive,
    "pastParticiple": pastparticiple,
    "presentParticiple": presentParticiple,
    
    "firstPersonPresent": firstPersonPresent,
    "secondPersonPresent": secondPersonPresent,
    "thirdPersonPresent": thirdPersonPresent,
    "firstPersonPluralPresent": firstPersonPluralPresent,
    "secondPersonPluralPresent": secondPersonPluralPresent,
    "thirdPersonPluralPresent": thirdPersonPluralPresent,

    "firstPersonPast": firstPersonPast,
    "secondPersonPast": secondPersonPast,
    "thirdPersonPast": thirdPersonPast,
    "firstPersonPluralPast": firstPersonPluralPast,
    "secondPersonPluralPast": secondPersonPluralPast,
    "thirdPersonPluralPast": thirdPersonPluralPast,

    "singularImperative": singularImperative,
    "pluralImperative": pluralImperative,
  }

def parseTerms2(htmlContent):
  # print("html:", htmlContent)
  normalClass = re.compile(r"(?<=<span class='\\\"normal\\\"'>)(.*?)(?=<\/span>)")
  nounDeclensions = normalClass.findall(htmlContent)
  # print(nounDeclensions)
  # noun = nounDeclensions[0]
  nominativeSingularIndefinite = nounDeclensions[1]
  nominativeSingularDefinite = nounDeclensions[2]
  nominativePluralIndefinite = nounDeclensions[3]
  nominativePluralDefinite = nounDeclensions[4]

  genitiveSingularIndefinite = nounDeclensions[5]
  genitiveSingularDefinite = nounDeclensions[6]
  genitivePluralIndefinite = nounDeclensions[7]
  genitivePluralDefinite = nounDeclensions[8]

  dativeSingularIndefinite = nounDeclensions[9]
  dativeSingularDefinite = nounDeclensions[10]
  dativePluralIndefinite = nounDeclensions[11]
  dativePluralDefinite = nounDeclensions[12]

  accusativeSingularIndefinite = nounDeclensions[13]
  accusativeSingularDefinite = nounDeclensions[14]
  accusativePluralIndefinite = nounDeclensions[15]
  accusativePluralDefinite = nounDeclensions[16]
  
  return {
    "nominativeSingularIndefinite": nominativeSingularIndefinite,
    "nominativeSingularDefinite": nominativeSingularDefinite, 
    "nominativePluralIndefinite": nominativePluralIndefinite,
    "nominativePluralDefinite": nominativePluralDefinite,
    "genitiveSingularIndefinite": genitiveSingularIndefinite,
    "genitiveSingularDefinite": genitiveSingularDefinite,
    "genitivePluralIndefinite": genitivePluralIndefinite,
    "genitivePluralDefinite": genitivePluralDefinite,
    "dativeSingularIndefinite": dativeSingularIndefinite,
    "dativeSingularDefinite": dativeSingularDefinite,
    "dativePluralIndefinite": dativePluralIndefinite,
    "dativePluralDefinite": dativePluralDefinite,
    "accusativeSingularIndefinite": accusativeSingularIndefinite,
    "accusativeSingularDefinite": accusativeSingularDefinite,
    "accusativePluralIndefinite": accusativePluralIndefinite,
    "accusativePluralDefinite": accusativePluralDefinite,
  }

def extractPresent(tensesList):
  tenses = []
  for item in tensesList:
    # print(item)
    pronoun = item.split("\' ")[0].replace("'", "")
    verb = item.split('>')[1].replace("'", "")
    conjugation = (f"{pronoun} {verb}", "irregular" if "irregular" in item else "regular")
    tenses.append(conjugation)

  return tenses
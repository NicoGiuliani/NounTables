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
    print(fetch)
    result = subprocess.check_output(fetch, shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
    selector = scrapy.Selector(text=result)
    html = selector.css('html body p div').get()
    # print(html)
    match = parseTerms(html) if html is not None else {}
    return Response(match)

  except subprocess.CalledProcessError as e:
    # Handle errors if the command fails
    error_message = f"Error executing command: {e.output}"
    print(error_message)
    return Response({"error": error_message}, status=500)
  

def parseTerms(htmlContent):
  # print("html:", htmlContent)
  normalClass = re.compile(r"(?<=<span class='\\\"normal\\\"'>)(.*?)(?=<\/span>)")
  nominalForms = normalClass.findall(htmlContent)
  infinitive = nominalForms[0]
  pastparticiple = nominalForms[1]
  presentParticiple = nominalForms[2]

  columnsSub = re.compile(r"(?<=$<table class='\\\"verbtense\\\"'>).|\n*?(?<=<span data-speech='\\\").*?(?=<\/span>)")
  tensesList = columnsSub.findall(htmlContent)
  presentTenses = extractPresent(tensesList)

  # print(presentTenses)
  
  return {
    "infinitive": infinitive,
    "pastParticiple": pastparticiple,
    "presentParticiple": presentParticiple
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
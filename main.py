import os
import PyPDF2
import re
import openai
from pymed import PubMed
from scholarly import scholarly

base_path = './pdf'
files = [] #a list of locally downloaded pdfs to summerize
summaries = []
pdf_summay_file = './summary.txt'

# Here we need to authenticate to services such as pubmed and cinahl and find studies based on keywords, and also take into account last time we summarized studies 
# so we dont summerize the same studies again

"""
pubmed = PubMed(tool="SummarizeStudiesWithChatGPT", email="my@email.address")
results = pubmed.query(""occupational health[Title]", max_results=10)

for article in results:
  # Extract and format information from the article
  article_id = article.pubmed_id
  title = article.title
  if article.keywords:
      if None in article.keywords:
          article.keywords.remove(None)
      keywords = '", "'.join(article.keywords)
  publication_date = article.publication_date
  abstract = article.abstract

  # Show information about the article
  print(
      f'{article_id} - {publication_date} - {title}\nKeywords: "{keywords}"\n{abstract}\n'
  )
"""



# Set the string that will contain the summary
for pdf in files:
  pdf_summary_text = ""
  # Open the PDF file
  pdf_file_path = "%s/%s" % (base_path, pdf)
  # Read the PDF file using PyPDF2
  pdf_file = open(pdf_file_path, 'rb')
  pdf_reader = PyPDF2.PdfReader(pdf_file)
  # Loop through all the pages in the PDF file
  for page_num in range(len(pdf_reader.pages)):
      # Extract the text from the page
      page_text = pdf_reader.pages[page_num].extract_text().lower()
      
      response = openai.ChatCompletion.create(
                      model="gpt-3.5-turbo",
                      messages=[
                          {"role": "system", "content": "You are a helpful research assistant."},
                          {"role": "user", "content": f"Summarize this: {page_text}"},
                              ],
                                  )
      page_summary = response["choices"][0]["message"]["content"]
      pdf_summary_text+=page_summary + "\n"
      
  summaries.append(pdf_summary_text)
  pdf_file.close()
  
#join the summaryfiles
with open(pdf_summary_file, "w+") as file:
  for document in summaries:
    file.write(document)

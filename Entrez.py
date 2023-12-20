from Bio import Entrez
from datetime import datetime


# Set your email for PubMed requests (required)
Entrez.email = "your_email_here"

# Keywords list to search in PubMed
keywords_list = ["supplements","aerobic"]

# Combine keywords with OR operator for PubMed query. you can also use AND
keywords_query = ' OR '.join(keywords_list)

# Get today's date in for the text file's name (YYYY/MM/DD)
today_date = datetime.today().strftime('%Y-%m-%d')


# All you need to search is the keywords query
search_query = f'({keywords_query})'

# Step 1: ESearch to get UIDs
#db stands for Database
#retmax means how many articles you want to retrieve
#datetype means what dates are you looking for. pdat means publication date
#reldate: This parameter limits the search to items that have a date within the last n days, where n is an integer

search_results = Entrez.read(Entrez.esearch(db="pubmed", term=search_query, retmax=20, datetype="pdat", reldate=20, usehistory="y"))
webenv = search_results['WebEnv']
query_key = search_results['QueryKey']
id_list = search_results['IdList']
#####################################


all_summaries=[]
# Step 2: EFetch to retrieve titles based on the UIDs
for i in id_list:
    fetch_handle = Entrez.efetch(db="pubmed",id=i, rettype="abstract", retmode="text", webenv=webenv, query_key=query_key)
    fetch_content = fetch_handle.read()
    all_summaries.append(fetch_content)  # Store title along with summary


# Generate file name with today's date
file_name = f"pubmed_summaries_{today_date}.txt"  # Added '.txt' extension

# Save all titles and summaries in a text file
with open(file_name, 'w', encoding='utf-8') as file:
    for content in all_summaries:
        file.write("################################################## \n\n")
        file.write(f"results: \n{content}\n\n")

print(f'Summaries saved in "{file_name}"')

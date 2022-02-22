import bs4
import requests

result = requests.get("https://dev.azure.com/AnaChem/AnaChemProjects/_queries/edit/38206/?triage=true")

print(type(result))
# print(result.text)

soup = bs4.BeautifulSoup(result.text, "lxml")
# print(soup)
print(soup.select('div'))
print(soup.select('P')[0].getText())

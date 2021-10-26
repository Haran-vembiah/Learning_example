import urllib.request

webUrl = urllib.request.urlopen("https://www.google.com")
print("Result code :" + str(webUrl.getcode()))
data = webUrl.read()  # retrieve the html page of the given Url
print(data)

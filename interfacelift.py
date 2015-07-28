from bs4 import BeautifulSoup
from subprocess import call
from appscript import app, mactypes
import os, re, requests, urllib, sys


ROOT_DOMAIN = "http://interfacelift.com"
RESOLUTION = "1366x768"
DOWNLOAD_LOCATION = "Scraped images/interfacelift"

DEBUGGING = False

def printDebug(message):
	if (DEBUGGING): print(message)


rawHomepage = requests.get(ROOT_DOMAIN)
homepageBS = BeautifulSoup(rawHomepage.text, "html.parser")
printDebug("Homepage downloaded.")


imageLabel = homepageBS.body.find_all("div", class_="wallpaper")[0]


imageIDSourceURL = "https://interfacelift.com/inc_NEW/jscript002.js"
imageIDSourceText = requests.get(imageIDSourceURL).text
imageIDLine = "document.getElementById('download_'+id).innerHTML = \"<a href=\\\"/wallpaper/"
imageIDIndex = imageIDSourceText.find(imageIDLine) + len(imageIDLine)
imageID = imageIDSourceText[imageIDIndex:imageIDIndex + 7]

printDebug("<id> part of path found: " + imageID)


imagePreviewURL = imageLabel.a.img["src"]
imageName = re.search("[0-9]{5}_[A-Za-z0-9]+_", imagePreviewURL).group()

printDebug("<imageName> parth of path found: " + imageName)


imageURL = "http://interfacelift.com/wallpaper/%s/%s%s.jpg" % (
					imageID, imageName, RESOLUTION)
printDebug("Final image URL: " + imageURL)


if not os.path.isdir(DOWNLOAD_LOCATION):
	printDebug("Download location not found. Creating " + DOWNLOAD_LOCATION)
	os.makedirs(DOWNLOAD_LOCATION)


localFileName = imageURL.split("/")[-1]
localFilePath = DOWNLOAD_LOCATION + "/" + localFileName
fileExists = os.path.isfile(localFilePath)

if (fileExists): printDebug("Current Interfacelift image already downloaded. Skipping download.")

if not fileExists:
	printDebug("Downloading file\n\tfrom: " + imageURL + "\n\tto: " + localFilePath)

	urllib.urlretrieve(imageURL, localFilePath)

	printDebug("File downloaded.")


sys.stdout.write(localFilePath)

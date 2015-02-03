import re, string
ARTE_CONCERT_URL	  = 'http://concert.arte.tv'
ARTE_URL	  = 'http://www.arte.tv'

ICON = 'arte_logo.png'
ART = 'art-default.png'

####################################################################################################
def Start():

  Plugin.AddPrefixHandler('/video/arte_tv', MainMenu, 'ARTE_TV', ICON, ART)
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  ObjectContainer.title1 = 'ARTE_TV'
  ObjectContainer.content = ContainerContent.GenericVideos
  ObjectContainer.art = R(ART)
  DirectoryObject.thumb = R(ICON)
  VideoClipObject.thumb = R(ICON)
  VideoClipObject.art = R(ART)
  HTTP.CacheTime = 1800

####################################################################################################
def MainMenu():

  oc = ObjectContainer(
    objects = [
      DirectoryObject(key = Callback(GetItemList, url='/fr', title2='Concerts French'), title = L('Arte Concerts French')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/fr/plus7.json', title2='Arte +7 French'), title = L('Arte +7 French')),
      DirectoryObject(key = Callback(GetItemList, url='/de', title2='Concerts German'), title = L('Arte Concerts German')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/de/plus7.json', title2='Arte +7 German'), title = L('Arte +7 German'))
    ]
  )                                 
  # append programs list directly
  # oc = GetProgramList(url="video/", oc=oc)
  return oc

####################################################################################################
	
def GetItemList(url, title2, page=''):
  Log ("ARTE GetItemList :" + url)
  Log.Exception('GetItemList')
  cookies = HTTP.CookiesForURL(ARTE_CONCERT_URL)
  oc = ObjectContainer(title2=title2, view_group='InfoList', http_cookies=cookies)
  Log.Exception('videos')
  program_url = ARTE_CONCERT_URL + url
  Log ("ARTE url : " + program_url)
  html = HTML.ElementFromURL(program_url)
  videos = html.xpath('//article')
  Log.Info(videos)
  for video in videos:
    Log.Info(video)
    try:
      video_page_url = ARTE_CONCERT_URL + video.xpath('.//div[contains(@class, "header-article")]/a/@href')[0]
      Log ("video url: " + video_page_url)
      title = unicode (video.xpath('.//div[contains(@class, "header-article")]//a/@title')[0])
      # Log ("title: " + title)
      img = video.xpath('.//div[contains(@class, "header-article")]//img/@src')[0]
      # Log ("img: " + img)
      oc.add(VideoClipObject(url = video_page_url, title = title, thumb=img))
    except:
      Log.Exception("error adding VideoClipObject")
      pass
        
  return oc

####################################################################################################

def GetPlus7Param (video, param, remove_slash, remove_spaces):
  result = video.split(param)[1].split(",")[0]
  # clean the url...
  result = result.split(":",1)[1]
  if remove_slash > 0:
    result = result.replace("\\", "")
  result = result.replace("\"", "")
  if remove_spaces > 0:
    result = result.replace(" ", "")
  return result
  
####################################################################################################
	
def GetPlus7ItemList(url, title2, page=''):
  Log ("ARTE GetPlus7ItemList :" + url)
  Log.Exception('GetPlus7ItemList')
  oc = ObjectContainer(title2=title2, view_group='InfoList')
  Log.Exception('videos')
  program_url = ARTE_URL + url
  Log ("ARTE +7 url : " + program_url)
  json = HTML.StringFromElement(HTML.ElementFromURL(program_url))
  json = json.split("[")[1].split("]")[0]
  videos = json.split("{")
  for video in videos:
    try:
      video_page_url = ARTE_URL + GetPlus7Param (video, "\"url\"", 1, 1)
      Log ("video url: " + video_page_url)
      title = GetPlus7Param (video, "\"title\"", 0, 0).decode("unicode_escape")
      # Log ("title: " + title)
      img = GetPlus7Param (video, "\"image_url\"", 1, 1)
      # Log ("img: " + img)
      oc.add(VideoClipObject(url = video_page_url, title = title, thumb=img))
    except:
      Log.Exception("error adding VideoClipObject")
      pass    
  return oc


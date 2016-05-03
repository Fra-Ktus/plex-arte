import re, string
ARTE_CONCERT_URL  = 'http://concert.arte.tv'
ARTE_URL  = 'http://www.arte.tv'

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
      DirectoryObject(key = Callback(GetConcertItemList, url='/fr', title2='Concerts French'), title = L('Arte Concerts French')),
      DirectoryObject(key = Callback(GetConcertPageItemList, url='/fr/videos/musiques-actuelles', title2='Concerts French Musiques Actuelles'), title = L('Arte Concerts French Musiques Actuelles')),
      DirectoryObject(key = Callback(GetConcertPageItemList, url='/fr/videos/musique-classique', title2='Concerts French Musique Classique'), title = L('Arte Concerts French Musique Classique')),
      DirectoryObject(key = Callback(GetConcertPageItemList, url='/fr/videos/jazz', title2='Concerts French Jazz'), title = L('Arte Concerts French Musique Jazz')),
      DirectoryObject(key = Callback(GetConcertPageItemList, url='/fr/videos/musiques-du-monde', title2='Concerts French Musiques Du Monde'), title = L('Arte Concerts French Musique Musiques Du Monde')),
      DirectoryObject(key = Callback(GetConcertPageItemList, url='/fr/videos/danse', title2='Concerts French Danse'), title = L('Arte Concerts French Danse')),
      DirectoryObject(key = Callback(GetPlus7MusicCollectionItemList, url='/fr/videos/all', title2='Concerts French Collections'), title = L('Arte Concerts French Collections')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/fr/plus7/', title2='Arte +7 French'), title = L('Arte +7 French')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/fr/plus7/actu-société', title2='Arte +7 French Actu'), title = L('Arte +7 French Actu')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/fr/plus7/séries-fiction', title2='Arte +7 French Series Fiction'), title = L('Arte +7 French Series Fiction')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/fr/plus7/cinéma', title2='Arte +7 French Cinema'), title = L('Arte +7 French Cinema')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/fr/plus7/arts-spectacles-classiques', title2='Arte +7 French Arts'), title = L('Arte +7 French Arts')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/fr/plus7/culture-pop', title2='Arte +7 French Culture Pop'), title = L('Arte +7 French Culture Pop')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/fr/plus7/découverte', title2='Arte +7 French Decouverte'), title = L('Arte +7 French Decouverte')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/fr/plus7/histoire', title2='Arte +7 French Histoire'), title = L('Arte +7 French Histoire')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/fr/plus7/junior', title2='Arte +7 French Junior'), title = L('Arte +7 French Junior')),
      DirectoryObject(key = Callback(GetConcertItemList, url='/de', title2='Concerts German'), title = L('Arte Concerts German')),
      DirectoryObject(key = Callback(GetPlus7ItemList, url='/guide/de/plus7/', title2='Arte +7 German'), title = L('Arte +7 German'))
    ]
  )                                 
  # append programs list directly
  # oc = GetProgramList(url="video/", oc=oc)
  return oc

####################################################################################################

def GetConcertItemList(url, title2, page=''):
  Log ("ARTE GetConcertItemList :" + url)
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

def GetConcertPageItemList(url, title2, page=''):
  Log ("ARTE GetConcertItemList :" + url)
  cookies = HTTP.CookiesForURL(ARTE_CONCERT_URL)
  oc = ObjectContainer(title2=title2, view_group='InfoList', http_cookies=cookies)
  Log.Exception('videos')
  page_num = 0
  while page_num < 10:
    program_url = ARTE_CONCERT_URL + url + "?page=" + str (page_num)
    page_num = page_num + 1
    Log ("ARTE url : " + program_url)
    html = HTML.ElementFromURL(program_url)
    videos = html.xpath('//article')
    if (len(videos)==0):
        break
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

def GetPlus7MusicCollectionItemList(url, title2, page=''):
  Log ("ARTE GetPlus7ItemList :" + url)
  oc = ObjectContainer(title2=title2, view_group='InfoList')
  program_url = ARTE_CONCERT_URL + url
  Log ("ARTE +7 music collection url : " + program_url)
  html = HTML.ElementFromURL(program_url)
  links = html.xpath('//div[contains(@id, "events")]//li')
  Log ("ARTE +7 music collection url, found %d links", len(links))
  for link in links:
    try:
      img = ""
      video_page_url = ""
      title = ""
      video_page_url = link.xpath('.//a//@href')[0]
      img = link.xpath('.//a/img//@src')[0]
      title = link.xpath('.//a/img//@title')[0]
      oc.add(DirectoryObject(key = Callback(GetConcertItemList, url=video_page_url, title2=title), title = title, thumb=img))

    except:
      Log.Exception("error adding VideoClipObject")
      pass

  return oc


####################################################################################################

def GetPlus7ItemList(url, title2, page=''):
  Log ("ARTE GetPlus7ItemList :" + url)
  oc = ObjectContainer(title2=title2, view_group='InfoList')
  program_url = ARTE_URL + url
  Log ("ARTE +7 url : " + program_url)
  html = HTML.ElementFromURL(program_url)
  scripts = html.xpath('//script')
  for script in scripts:
    script_text = HTML.StringFromElement(script)
    try:
      img = ""
      video_page_url = ""
      title = ""
      script_lines1 = script_text.split('{')
      for script_line1 in script_lines1:
        script_lines2 = script_line1.split('}')
        for script_line2 in script_lines2:
          script_lines3 = script_line2.split(',')
          for script_line3 in script_lines3:
            # Log ("Line : " + script_line3)
            if (script_line3.find("\"url\"") > -1):
              if (script_line3.find(".jpg") > -1):
                img = GetPlus7Param (script_line3, "\"url\"", 1, 1)
            if (script_line3.find("\"title\"") > -1):
              title = GetPlus7Param (script_line3, "\"title\"", 0, 0).decode("unicode_escape")
            if (script_line3.find("\"url\"") > -1):
              if (script_line3.find("autoplay") > -1):
                video_page_url = GetPlus7Param (script_line3, "\"url\"", 1, 1)
                oc.add(VideoClipObject(url = video_page_url, title = title, thumb=img))

    except:
      Log.Exception("error adding VideoClipObject")
      pass

  return oc


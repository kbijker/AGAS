import flickrapi
import urllib.request
import os

def fotozoek(onderwerp):
    os.chdir('C:\sqlite/acgas/app/fotos')

    api_key = '95f2a5415ec530e526fb2bbc6e727ca8'
    api_secret = '4f5d97cc03b8d31a'
    try:
       flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
       photos = flickr.photos.search(text = onderwerp, per_page=3)

       for photo in photos['photos']['photo']:
          url = 'https://farm{}.staticflickr.com/{}/{}_{}.jpg'.format(photo['farm'], photo['server'], photo['id'], photo['secret'])
          urllib.request.urlretrieve(url, '{}.jpg'.format(photo['id']))
       return 'Flickr zoekt naar afbeeldingen.'
    except:
       return 'code 503? Geen connectie met Flickr.com'

#respons = fotozoek('watertor')
#print(respons)

"""
API=key:
https://www.flickr.com/services/api/misc.api_keys.html

e-mail, ww W..@@
"""
# simple action can be write down here
# for simple thing like email validator
# curency format
# etc, simple thing write down here

import re
import urllib.request
import json
import datetime
import time
import cgi
import base64
import math
from urllib.parse import quote
from urllib.parse import unquote

# for auto rotate need python pillow or PIL
import os
from PIL import Image

import traceback

class Utility():
    # constructor
    def __init__(self):
        
    # email format validator
    # parameter should be email address in string format
    # if valid will return true
    # if not valid will return none
    # if valid will return regex match object
    # return value is tuple
    # (True/False, message)
    def validate_email_format(self, email):
        if re.match('[a-zA-Z0-9._%-]+[@][a-zA-Z0-9._%-]+[.][a-zA-Z]+', email):
            return (True, 'Ok:val_em_1:Email is in well formed format')
        
        return (False, 'error:val_em_1:Email format must be in well formed format, like \'yourname@mydomain.com\'')
        
    # validate password length
    # and password strength
    # password should not be less than 6 of character
    # return value is tuple (True/False, 'message)
    def validate_password_format(self, password):
        if len(password) < 6:
            return (False, 'error:val_pass_1:Password can\'t be less than 6 characters')
        
        
        # check password strength
        upper_char = re.search('[A-Z]', password)
        lower_char = re.search('[a-z]', password)
        num = re.search('[0-9]', password)
        special_char = re.search('[^a-zA-Z0-9]', password)
        
        if upper_char and lower_char and num and special_char:
            return (True, 'ok:val_pass_1:Password is great')

        else:
            return (False, 'error:val_pass_2:Password must be contains uppercase character, lowercase character, number and special character. Example \'Hel0#W33n\'')
            
    # get base domain
    def get_base_domain(self, link):
        
        # remove :// protocol
        lnk = link.split('://')
        if len(lnk) > 1:
            lnk = lnk[1].strip()
            
        else:
            lnk = lnk[0].strip()
            
        # remove depth section /
        lnk = lnk.split('/')[0].strip()
        
        return lnk
    
    # link format should be domain.com
    # or subdomain.domain.com
    # regex check format '[a-zA-Z0-9_%-.]+[.][a-zA-Z0-9_%-.]+'
    # will return base domain name
    def validate_link_format(self, link):
        # remove :// protocol
        lnk = link.split('://')
        if len(lnk) > 1:
            lnk = lnk[1].strip()
            
        else:
            lnk = lnk[0].strip()
            
        # remove depth section /
        lnk = lnk.split('/')[0].strip()
        
        base_domain = re.search('[a-zA-Z0-9_%-.]+[.][a-zA-Z0-9_%-.]+', lnk)
        
        if base_domain:
            return base_domain.group()
            
        return None
    
    # check if file active and accessible
    # parameter is link with protocol
    # ex: http://facebook.com
    # will return urlopen object result
    def validate_link(self, link):
        protocol = link.find('://')
        
        if protocol != -1:
            req = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"})
            url_page = urllib.request.urlopen(req)
            return url_page
        else:
            for prot in ('http://', 'https://'):
                req = urllib.request.Request(prot + link, headers={'User-Agent' : "Magic Browser"})
                url_page = urllib.request.urlopen(req)
                return url_page

    # get go ip data
    # trying from
    # http://www.telize.com/geoip/46.19.37.108
    def get_geoip4_info(self, ip4):
        data = urllib.request.urlopen(''.join(('http://www.telize.com/geoip/', ip4))).readall().decode('UTF-8').strip()

        # validate data is json format
        json.loads(data)

        return data

    # get month list
    # will return ['Jan', 'Feb' ... 'Dec']
    def get_list_month(self):
        month = []
        for i in range(1, 13):
            month.append(datetime.datetime(2015, i, 1).strftime('%b'))
            
        return month

    # generator
    # for unique seed
    # parameter must be in integer
    def generate_unique(self, seed):
        unique_seed = ('q', 'i', 'G', 'Y', 'J', 'W', '9', 'L', 's', 'a', 'O', 'T', '6', '_', 'K', 'd', '2', 'p', 'Z', 'k', 'v', 'B', '7', 'C', 'm', 'M', 'Q', 'y', 'b', 'V', 'X', '8', '0', 'F', 'w', '4', '1', 'E', 'n', 'j', 'c', 'g', 'R', 'U', 'I', 'f', 'u', 'l', 'N', 'D', 'A', '3', 'x', 'o', 'H', 'P', 'h', '5', 'z', 'S', 'r', 'e', 't', '-')

        # limit to 32 long
        # generate depend on unique_seed
        val = seed
        unique_chunk = []
        for i in range(0, 32):
            letter = val & 63
            unique_chunk.append(letter)
            val = val >> 6
        
        # reverse chunk
        # then remove leading zero
        unique_chunk.reverse()
        for i in unique_chunk[:]:
            if i:
                break
        
            unique_chunk.pop(i)
        
        for i in range(0, len(unique_chunk)):
            unique_chunk[i] = unique_seed[unique_chunk[i]]
        
        return ''.join(unique_chunk)

    # get html head info
    # will return dictionary
    # contain html head info
    # parameter is html page source
    def get_html_head_info(self, html):

        # properties return value
        properties = {}

        # parse html source and get
        # link tag
        # meta tag
        # title tag
        properties['link'] = re.findall('<[\s]*(?i)link[\s]*[\w\'\"%_%-=/:._\s;%-%+%?%{%}]*>', html)
        properties['meta'] = re.findall('<[\s]*(?i)meta[\s]*[\w\'\"%_%-=\w/:._\s;%-%+%?%{%}]*>', html)
        properties['title'] = ''

        html_title = re.search('<[\s]*title[\s]*>[\w\W\'\"=/:._\s;%-%+%?%{%}]*[\s]*<[\s]*/[\s]*title[\s]*>', html)
        html_title = re.findall('<[\s]*(?i)title[\s]*>[\w\W\'\"=/:._\s;%-%+%?%{%}]*[\s]*<[\s]*/[\s]*(?i)title[\s]*>', html)
        
        if html_title:
            properties['title'] = html_title[0]
    
        return properties

    # will return series of date time step in list strftime string format
    # parameter is
    # time_epoch is datetime convert to epoch time should be in int format or it can be int(datetime.datetime.today().strftime('%s')) # should be in second
    # offset is time to be decrement or increment it depend on backward
    # if backward is Trus it will produce date time step backward time with offset decrement
    # if backward is False it will produce date time step forward time with ottset increment
    # ex : get_datetime_step(time.time(), 3600, 5, True)
    # will produce ['2015-03-25 13:01:06', '2015-03-25 12:12:06', '2015-03-25 11:11:06', '2015-03-25 10:10:06', '2015-03-25 09:09:06']
    def get_datetime_step(self, time_epoch, offset, step=5, backward=True):
        datetimes = []
        datetime_step = time_epoch

        if backward:
            for index in range(0, step):
                datetimes.append(time.strftime("%Y-%m-%d %H:%I:%S", time.localtime(datetime_step)))
                datetime_step -= offset

        else:
            for index in range(step, 0, -1):
                datetimes.append(time.strftime("%Y-%m-%d %H:%I:%S", time.localtime(datetime_step)))
                datetime_step += offset

        return datetimes

    # check if object is dictionary type
    def is_dict_type(self, obj):
        return type(obj).__name__ == 'dict'

    # check if object is bool type
    def is_bool_type(self, obj):
        return type(obj).__name__ == 'bool'

    # check if object is tuple type
    def is_tuple_type(self, obj):
        return type(obj).__name__ == 'tuple'

    # check if object is list type
    def is_list_type(self, obj):
        return type(obj).__name__ == 'list'
        
    # strip html
    # strip html tags
    def html_strip_tags(self, text):
        return re.sub('<[^<]+?>', '', text)
        
    # html escape
    def html_escape(self, text):
        return cgi.escape(text).replace('\'', '&#39;').replace('"', '&#34;')

    def resize_image(self, image, resize=(), resample=Image.ANTIALIAS, scale='down'):
        size = image.size
        image_orientation = self.get_orientation_image(image)
        if not len(resize):
            return None

        width = 0
        height = 0
        
        if len(resize) == 1:
            width = resize[0]
        else:
            width = resize[0]
            height = resize[1]
        
        # if resize only give one use ratio to resize
        # automatic resize
        if not height:
            ratio = 0
            # landscape mode
            if image_orientation == 'landscape':
                ratio = width / size[0] # get ratio resize as lanscape
            # portrait ratio
            if image_orientation == 'portrait':
                ratio = width / size[1] # get height ratio
            if ratio > 0:
                width = round(size[0] * ratio)
                if not width: # if width resize equals to 0 use original width
                    width = size[0]
                height = round(size[1] * ratio)
                if not height: # if height resize equals to 0 use original height
                    height = size[1]

        # check scale
        if scale == 'down':
            if image_orientation == 'landscape' and width >= size[0]:
                return None
                
            if image_orientation == 'portrait' and width >= size[1]:
                return None
            
        if scale == 'up':
            if image_orientation == 'landscape' and width <= size[0]:
                return None
                
            if image_orientation == 'portrait' and width <= size[1]:
                return None

        # do resize only if width and height
        if width and height:
            return image.resize((width, height), resample=resample)
            
        return None
        
    # check image orientation
    def get_orientation_image(self, image):
        size = image.size
        if size[0] > size[1]:
            return 'landscape'
        if size[0] < size[1]:
            return 'portrait'
    
    # auto rotate image if have exif tags
    def autorotate_image(self, path, resize=(), quality=10, resample=Image.ANTIALIAS, scale='down'):
        """ This function autorotates a picture """
        try:
            image = Image.open(path)
            exif = image._getexif()
            if not exif:
                return False
        
            orientation_key = 274 # cf ExifTags
            if orientation_key in exif:
                orientation = exif[orientation_key]
        
                rotate_values = {
                    3: 180,
                    6: 270,
                    8: 90
                }
        
                if orientation in rotate_values:
                    # Rotate and save the picture
                    image = image.rotate(rotate_values[orientation])
                    rimage = self.resize_image(image, resize=resize, resample=resample, scale=scale)
                    if rimage:
                        image = rimage
                    image.save(path, quality=quality)
                    image.close()
                    return True
                    
            image.close()
        except:
            return False
        
    # reduce quality
    # default reduce 20% quality
    def reduce_quality_image(self, path, resize=(), quality=10, resample=Image.ANTIALIAS, scale='down'):
        image = Image.open(path)
        rimage = self.resize_image(image, resize=resize, resample=resample, scale=scale)
        if rimage:
            image = rimage
        image.save(path, quality=quality)
        image.close()
        
# -*- coding: utf-8 -*-
# Copyright 2012 Mandla Web Studio
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'Jose Maria Zambrana Arze'
__email__ = 'contact@josezambrana.com'
__version__ = '0.1'
__copyright__ = 'Copyright 2012, Mandla Web Studio'


import logging

from django import template
from django.conf import settings


register = template.Library()


def thumbnail_url(obj, size='s'):
    """
    Retorna la url del thumbnail
    """

    if size not in obj.sizes:
        raise ValueError('%s is not a valid size' % size)

    if not obj.thumbnail_exists(size):
        url = obj.default_thumbnail(size)
    else:
        url = obj.thumbnail_url(size)
    
    return url

register.simple_tag(thumbnail_url)


def thumbnail_original(obj):
    """
    Retorna el url de la imagen original.
    """

    return obj.image.url

register.simple_tag(thumbnail_original)


def thumbnail_img(obj, size='s'):
    """
    Retorna el html tag img del thumbnail.
    """
    return "<img src='%s' alt='%s' class='img-avatar' />" % thumbnail_url(obj, size)

register.simple_tag(thumbnail_img)


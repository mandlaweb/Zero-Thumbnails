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
__copyright__ = 'Copyright 2012, Mandla Web Studio'


import logging

from django.conf import settings
from django.core.files.base import ContentFile

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from PIL import Image
except ImportError:
    import Image


THUMBNAIL_RESIZE_METHOD = getattr(settings, 'THUMBNAIL_RESIZE_METHOD', Image.ANTIALIAS)


class BaseMethodThumbnail(object):
    """
    Clase base para los métodos para generar thumbnails thumbnails.
    """
    
    method = THUMBNAIL_RESIZE_METHOD

    @classmethod
    def apply(cls, image, width, height):
        """
        Aplica el método para generar el thumbnail.
        """

        raise NotImplementedError
    
    @classmethod
    def generate(cls, image, width, height):
        """
        Genera el thumbnail.
        """
        
        image = cls.apply(image, width, height)
        
        if image.mode != "RGB":
            image = image.convert("RGB")

        thumb = StringIO()
        image.save(thumb, "JPEG")
        return thumb


class ResizeThumbnail(BaseMethodThumbnail):
    """
    Genera un thumbnail edimensionando la imagen y manteniendo las proporciones.
    """
    
    method = Image.BILINEAR
    
    @classmethod
    def apply(cls, image, width, height=None):
        (w, h) = image.size
        
        if width < w:
            proportion = float(width) / float(w)
            height = int(proportion * float(h))
            image = image.resize((width, height), cls.method)

        return image


class CropThumbnail(BaseMethodThumbnail):
    """
    Genera un thumbnail cortado de los tamaños especificados
    """

    @classmethod
    def apply(cls, image, width, height):
        (w, h) = image.size
        
        f_w, f_h = float(w), float(h)
        f_width, f_height = float(width), float(height)

        if f_w > f_h:
            right_x = (f_width * f_h)/(f_height * f_w)
            bottom_y = 1.0
            if right_x > 1.0:
                bottom_y = 1.0 / right_x
                right_x = 1.0
        else:
            right_x = 1.0
            bottom_y = (f_height * f_w)/(f_width * f_h)
            if bottom_y > 1.0:
                right_x = 1.0 / bottom_y
                bottom_y = 1.0
        
        image = image.crop((0, 0, int(f_w * right_x), int(f_h * bottom_y)))
        image = image.resize((width, height), cls.method)

        return image


class SquareThumbnail(CropThumbnail):
    """
    Genera un thumbnail cuadrado.
    """

    @classmethod
    def apply(cls, image, width, height=None):
        (w, h) = image.size

        if height is None:
            height = width
        else:
            if w > h:
                width = height
            else:
                height = width
            
        return super(SquareThumbnail, cls).apply(image, width, height)

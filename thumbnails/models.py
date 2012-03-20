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


import os
import logging

from django.db import models
from django.core.exceptions import SuspiciousOperation
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from thumbnails.methods import SquareThumbnail
from common.util import log_time


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from PIL import Image
except ImportError:
    import Image


THUMBNAIL_RESIZE_METHOD = getattr(settings, 'THUMBNAIL_RESIZE_METHOD', Image.ANTIALIAS)


class ThumbnailMixin(models.Model):
    """
    Mixin para agregar thumbnails a un modelo.
    """
    
    #: imagen avatar sin redimensionar
    image = models.ImageField(verbose_name=_('Thumbnail'), max_length=5120,
                              upload_to='thumbnails', blank=True, null=True)
    #: generador de avatares
    method = SquareThumbnail

    #: dimensiones permitidas
    sizes = {
        'u': (65, 30),
        's': (120, 55),
        'm': (320, 145),
        'l': (500, 227)
    }

    #: Método para crear el thumbnail por cada tamaño.
    methods = {
        'u': SquareThumbnail,
        's': SquareThumbnail,
        'm': SquareThumbnail,
        'l': SquareThumbnail,
    }

    #: Nombres de los avatares por defecto.
    defaults = {
        'u': 'default_u.jpg',
        's': 'default_s.jpg',
        'm': 'default_m.jpg',
        'l': 'default_l.jpg',
    }

    #: path base
    basepath = ''

    
    class Meta:
        abstract = True
    
    def default_thumbnail(self, size):
        """
        Retorna el path del thumbnail por defecto.
        """
        
        if size not in self.defaults:
            raise ValueError('%s is not a valid size')

        thumb_name = self.defaults.get(size)
        return os.path.join(settings.STATIC_URL, self.thumbnail_basepath(), thumb_name)

    def create_thumbnails(self):
        """
        Crear los thumbnails para todas dimensiones
        """
        
        initial = log_time("create_thumbnails")
        sizes = sorted(self.sizes.items(), key=lambda x: x[1][0], reverse=True)
        last = None
        
        for name, dimension in sizes:
            self.create_thumbnail(name, last=last)
            last = name
            assert self.thumbnail_exists(name)

        log_time("end create_thumbnails", initial=initial)
            
    def create_thumbnail(self, size, last=None):
        """
        Crea el thumbnail para el tamaño *size*.
        """
        
        initial = log_time("thumbnail: %s" % size, indent=4)

        # Abrimos la imagen
        try:
            name = self.image.name if last is None else \
                   self.thumbnail_name(last)
            data = self.image.storage.open(name, 'rb').read()
            img = Image.open(StringIO(data))
        except IOError, e:
            logging.error('IOError: %s ' % e)
            return
        except SuspiciousOperation, e:
            logging.error('SuspiciousOperation: %s ' % e)
            return 
        
        # Obtenemos las dimensiones.
        if size not in self.sizes:
            raise ValueError('%s is not a valid size' % size)
        (width, height) = self.sizes.get(size)
        
        # Obtenemos el método para generar el thumbnail.
        if size not in self.methods:
            raise ImproperlyConfigured('%s is not present in methods' % size)
        method = self.methods.get(size)

        # Generamos el thumbnail
        thumb = method.generate(img, width, height)
        
        if thumb is not None:
            thumb_file = ContentFile(thumb.getvalue())
        else:
            thumb_file = ContentFile(data)
        
        # Escribimos el thumbnail en el disco
        name = self.thumbnail_name(size)
        if self.image.storage.exists(name):
            self.image.storage.delete(name)
            
        self.image.storage.save(name, thumb_file)
        log_time("end thumbnail", initial=initial, indent=4)
 
    def thumbnail_url(self, size):
        """
        Retorna el url del thumbnail de tamaño *size*
        """
        return self.image.storage.url(self.thumbnail_name(size))

    def thumbnail_basepath(self):
        """
        Retorna el path donde se almacena el thumbnail.
        """

        return getattr(settings, 'THUMBNAIL_STORAGE_DIR', self.basepath)

    def thumbnail_name(self, size):
        """
        Retorna el nombre del thumbnail de tamaño *size*
        """

        path = self.thumbnail_basepath()

        if self.image.name is not None:
            return os.path.join(path, str(size), self.image.name)

        return None
            
    def thumbnail_exists(self, size):
        """
        Verifica si el thumbnail para el tamaño *size* existe.
        """
        
        thumbnail_name = self.thumbnail_name(size)
        return self.image.storage.exists(thumbnail_name)
        

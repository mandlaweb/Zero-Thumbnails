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


import os
import logging

from django.conf import settings
from django.test import TestCase
from django.db import models
from django.core.files.base import ContentFile

from common.tests import TestBase

from thumbnails.models import ThumbnailMixin


IMAGE_TEST = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          'static', 'test.png')

class Article(ThumbnailMixin):
    title = models.CharField(max_length=255)


class ThumbnailsTest(TestBase):
    def setUp(self):
        super(ThumbnailsTest, self).setUp()
        self.article = Article(title='ejemplo')
        self.image = open(IMAGE_TEST, 'r+')
        
    def test_create_thumbnails(self):
        """
        El sistema debe ser capaz almacenar un thumbnail dentro de un objeto.
        """
        
        logging.info('create_thumbnail')
        
        for size in self.article.sizes.keys():
            assert not self.article.thumbnail_exists(size)

        self.article.image.save('avatar.png', ContentFile(self.image.read()))
        self.article.create_thumbnails()
        
        for size in self.article.sizes.keys():
            assert self.article.thumbnail_exists(size)
    
    def test_default_thumbnail(self):
        """
        El sistema debe ser capaz de retornar un thumbnail por defecto.
        """

        for size in self.article.sizes.keys():
            assert self.article.default_thumbnail(size) is not None

    def test_thumbnails_url(self):
        """
        El sistema debe ser capaz de retornar la url de un thumbnail y todos
        sus tamaños.
        """

        logging.info('***** test_thumbnails_url *****')

        self.article.image.save('avatar.png', ContentFile(self.image.read()))
        self.article.create_thumbnails()

        for size in self.article.sizes.keys():
            url = self.article.thumbnail_url(size)
            logging.info('url: %s ' % url)
            assert url is not None

    def test_thumbnail_templatetag(self):
        """
        El sistema debe ser capaz de generar la url para un thumbnail en el 
        template
        """

        from thumbnails.templatetags.thumbnails_tags import thumbnail_url
        
        # Probamos que retorne la url por defecto
        url = thumbnail_url(self.article)
        assert url is not None
        logging.info('url: %s ' % url)

        # Probamos que retorne la url de un avatar subido.
        self.test_create_thumbnails()
        thumbnail_url = thumbnail_url(self.article)
        assert thumbnail_url is not None
        logging.info('thumbnail_url: %s ' % thumbnail_url)
        assert url != thumbnail_url

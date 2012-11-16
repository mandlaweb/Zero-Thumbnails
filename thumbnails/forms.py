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

from django import forms
from django.utils.safestring import mark_safe


class ThumbnailFileInput(forms.FileInput):
    def render(self, name, value, attrs=None):
        html = super(ThumbnailFileInput, self).render(name, value, attrs=attrs)

        logging.info('INPUT.class: %s' % value.__class__)

        #if value is not None:
        #    thumbnail_html = "<div class=\\"avatar span\\"><img src=\\"%s\\" class='img-avatar'/></div>%s"
        #    thumbnail_html = thumbnail_html % (value.thumbnail_url('s'), html)
        #    return mark_safe(thumbnail_html)

        return mark_safe(html)


class ThumbnailField(forms.FileField):
    widget = ThumbnailFileInput

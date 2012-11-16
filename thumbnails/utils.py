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


from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from thumbnails import MAX_THUMBNAIL_SIZE


def validate_file_size(f, max_allowed_size=MAX_THUMBNAIL_SIZE):
    """
    Check the file size of f is less than max_allowed_size
    """
    
    if f.size > max_allowed_size:
        message = _(u'"%s" is too large (%sKB), the limit is %sKB') % (
            f.name, f.size >> 10, max_allowed_size >> 10)
        raise ValidationError(message)

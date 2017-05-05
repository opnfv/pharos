##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from django.contrib import admin

from dashboard.models import *

admin.site.site_header = "Pharos Dashboard Administration"
admin.site.site_title = "Pharos Dashboard"

admin.site.register(Resource)
admin.site.register(Server)
admin.site.register(ResourceStatus)

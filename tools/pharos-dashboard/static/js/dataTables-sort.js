/*****************************************************************************
* Copyright (c) 2016 Max Breitenfeldt and others.
*
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Apache License, Version 2.0
* which accompanies this distribution, and is available at
* http://www.apache.org/licenses/LICENSE-2.0
*****************************************************************************/


/**
 * This is a sort function for dataTables to sort tables by the status column.
 * The order should be: online < online/idle < offline
 */
jQuery.extend(jQuery.fn.dataTableExt.oSort, {
    "status-pre": function (a) {
        switch (a) {
            case 'online':
                return 1;
            case 'online / idle':
                return 2;
            case 'offline':
                return 3;
            default:
                return a;
        }
    },

    "status-asc": function (a, b) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "status-desc": function (a, b) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});
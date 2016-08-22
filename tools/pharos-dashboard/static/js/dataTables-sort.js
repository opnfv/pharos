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
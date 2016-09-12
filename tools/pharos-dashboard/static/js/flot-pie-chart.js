function loadChartData(chart_id, url) {
    $.ajax({
        url: url,
        type: 'get',
        success: function (data) {
            var data = data['data'];
            $(function () {
                var plotObj = $.plot($("#" + chart_id), data, {
                    series: {
                        pie: {
                            show: true
                        }
                    }
                });
            });
        },
        failure: function (data) {
            alert('Error loading data');
        }
    });

}
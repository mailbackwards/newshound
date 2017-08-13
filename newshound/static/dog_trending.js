django.jQuery(function($) {
    var $target = $('#content-main');    // element to put the container before

    function makeContainer() {
        var $container = $('<div>' +
                              '<h2>Trending dogs</h2>' +
                              '<p><a href="#" class="button" id="trending-refresh">Refresh suggestions</a></p>' +
                              '<div id="trending"></div>' +
                           '</div><br /><hr />');
        $container.insertBefore($target);
    };

    function writeResults(results) {
        var html = '<table>';
        for (var i = 0; i < results.length; i++) {
            html += '<tr><td><img src="' + results[i].photo + '" height="50px" width="100px"></td><td>' + results[i].name + '</td><td>' + results[i].breeds + '</td></tr>'
        }
        html += '</table>';
        $('#trending').html(html);
    }

    function refreshAPI(results) {
        var url = window.location.pathname + 'trending/'  // hack
        $.ajax({url: url, method: 'get', success: function(data) {
            writeResults(data.results);
        }});
    }

    $(document).ready(function() {
        makeContainer();
        refreshAPI();
        $(document).on('click', '#trending-refresh', refreshAPI);
    })
});

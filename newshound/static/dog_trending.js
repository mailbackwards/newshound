django.jQuery(function($) {
    var $target = $('#content');    // element to put the container before

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
        for (var i = 0; i < results.dogs.length; i++) {
            var dog = results.dogs[i]
            html += '<tr><td>' + dog.name + '</td><td>' + dog.breeds + '</td><td><img src="' + dog.photo + '" height="50px" width="100px"></td></tr>'
        }
        html += '</table>';
        $('#trending').html(html);
    }

    function refreshAPI(results) {
        var url = window.location.pathname + 'trending/'  // hack
        $.ajax({url: url, method: 'get', success: function(data) {
            writeResults(data);
        }});
    }

    $(document).ready(function() {
        // not on changelist views
        if (window.location.pathname.split('/').length != 5) {
            makeContainer();
            refreshAPI();
            $(document).on('click', '#trending-refresh', refreshAPI);
        }
    })
});

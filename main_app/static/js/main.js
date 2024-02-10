//import _ from 'lodash';
//import '../css/base.css';

// Import Bootstrap scripts (order matters)
//import 'jquery';
//import 'popper.js';
//import 'bootstrap';


$(document).ready(function() {
    $('.subscribe-button').click(function(e) {
        e.preventDefault();

        var form = $('#subscribe-form');
        var csrfToken = $('input[name=csrfmiddlewaretoken]', form).val();

        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: csrfToken
            },
            success: function(data) {
                // upload state of bottom
                if (data.is_subscribed) {
                    $('.subscribe-button').text('Unsubscribe');
                } else {
                    $('.subscribe-button').text('Subscribe');
                }
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});


$(document).ready(function() {
    $('.like-button, .dislike-button').click(function() {
        var button = $(this);
        var postId = button.data('post-id');
        var isLike = button.hasClass('like-button');
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/main_app/' + postId + '/like-dislike/',
            type: 'POST',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: csrfToken,
                is_like: isLike ? 'true' : 'false',
            },
            success: function(data) {
                // Upload count of likes/dislikes
                $('#likes-count-' + postId).text(data.likes_count);
                $('#dislikes-count-' + postId).text(data.dislikes_count);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});
/**
 * Created with PyCharm.
 * User: vladimirtsyupko
 * Date: 08/09/2014
 * Time: 21:47
 * To change this template use File | Settings | File Templates.
 */

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length,c.length);
    }
    return "";
}

$(function(){

    var comment_name = getCookie('comment_name'),
        comment_text = getCookie('comment_text');

    if (comment_name && comment_text) {
        $('#comment_form').remove();
        $('#comment_results').html('<p>Name: <span>' + comment_name + '</span></p>' + '<p>Comment: <span>' + comment_text + '</span></p>');

    }

    $('#comment').on('click', function(){
        var comment_text = $('#comment_text').val(),
        comment_name = $('#comment_name').val();
        if(comment_name && comment_text){
            setCookie('comment_name', comment_name, 1/24/60); // 1 minute
            setCookie('comment_text', comment_name, 1/24/60); // 1 minute
            $('#comment_form').remove();
            $('#comment_results').html('<p>Name: <span>'+comment_name+'</span></p>'+'<p>Comment: <span>'+comment_text+'</span></p>');
        }

    });
});
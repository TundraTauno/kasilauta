// Toggle image between original and thumbnail
$(document).ready(function() {
    $("img").click(function() {
      var current = $(this).attr("src");
      var orig = $(this).siblings("ul").children("li.orig-img").text();
      var thumb = $(this).siblings("ul").children("li.thumb-img").text();
      $(this).attr("src", current === orig ? thumb : orig);
    });    
});

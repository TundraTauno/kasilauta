// Toggle image between original and thumbnail
$(document).ready(function() {
    $("img").click(function() {
      var current = $(this).attr("src");
      var orig = $(this).siblings("ul").children("li.orig-img").text();
      var thumb = $(this).siblings("ul").children("li.thumb-img").text();
      $(this).attr("src", current === orig ? thumb : orig);
    });    
});

// Linkify ids. This makes naive assumption that all ids are in the same thread.
// This doesn't matter, since this is the case 99 % of the time and we can later
// handle the "non-local" redirection.
$(document).ready(function() {
  $("p.post-text").each(function() {
    link_prefix = '<a href=#';
    link_postfix = '</a>';
    var regex = /(^|\W)>>\d{1,11}/g;

    matches = [];
    while ((match = regex.exec($(this).text())) !== null) {
      matches.push(match[0].trim());
    }

    var content = $(this).text();
    matches.forEach(function(match) {
      var replace_with = link_prefix + match.substr(2) + '>' + match + link_postfix;
      content = content.replace(new RegExp(match, 'g'), replace_with);
//       console.log('Replace ' + match + ' -> ' + replace_with);
    });
    $(this).html(content);
  })
});

// Follow reply links.
// TODO: Implement non-local redirection. 
$(document).ready(function() {
    var regex = /(^|\W)>>\d{1,11}/;
    $("p.post-text a").click(function(event) {
      var clicked = $(event.target).text().match(regex);
      if (clicked) {
        var number = clicked[0].substr(2);
        if ($('#' + number).length == 0)  // not a local link TODO: implement redirection.
          alert("Not a local link.");
        else
          $('#' + number).click();        // local link, go to post
      }
//       console.log(number[0].substr(2));
    });    
});

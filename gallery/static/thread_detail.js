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

// Popup dialog on hovering reply.
// TODO: Not working properly.
$(document).ready(function() {
  
  var regex = /(^|\W)>>\d{1,11}/;

  $("div.post-container div p.replies a, div.post-container div p.post-text a")
  .hover(function(event) {
      var hovered = $(event.target).text().match(regex);
      if (hovered) {
        var number = hovered[0].substr(2);
        if ($('#' + number).length == 0) {  // not a local link TODO: implement redirection.
//           console.log("Hovering on non-local link.");
          popup.dialog({ autoOpen: false }); // dummy placeholder for future
        }
        else { // local link, show popup to user
//           console.log("Hovering on local link."); 
          popup = $('#' + number).clone(false).prop("id", "temporary-id");
          popup.dialog({
              position: { my: "left bottom", at: "event", of: $(this)},
              classes: { "ui-dialog": "hide-close-btn hide-title popup-post" },
              modal: true
          });
        }
      }
    return false;
  },
    function(event) {
      popup.dialog('destroy').remove();
    }
  );
});


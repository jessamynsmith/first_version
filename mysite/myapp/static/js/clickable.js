    $(".clickable").click(function(e){
        var clicked = $(this);

         s = window.getSelection();
         var range = s.getRangeAt(0);
         var node = s.anchorNode;
         while(range.toString().indexOf(' ') != 0) {
            range.setStart(node,(range.startOffset -1));
         }
         range.setStart(node, range.startOffset +1);
         do{
           range.setEnd(node,range.endOffset + 1);

        }while(range.toString().indexOf(' ') == -1 && range.toString().trim() != '');
        var str = range.toString().trim();

        console.log(str);


        var datoajax = {palabra:str.toLowerCase()};
        console.log(datoajax);


        /* $.ajax({
            url: '/api/v1/words/?english_text=' + str.toLowerCase(),
            type: 'get', // This is the default though, you don't actually need to always mention it
            /*success: function(data) {
                console.log(data);
                if (data.length > 0) {
                    clicked.html(clicked.html().replace(str, data[0].spanish_text));
                } else {
                    alert('The word "' + str + '" is not in the translations database');
                }

            },
            failure: function(data) {
                alert('Got an error dude');
            }
        });*/
        $.ajax({
            url: '/wordajax/' ,
            type: 'GET', // This is the default though, you don't actually need to always mention it
            data: datoajax,
            success: function(data) {

                    console.log(data);
                    console.log(data.spanish_text);
                    var replacement = data.spanish_text;
                    clicked.html(clicked.html().replace(str, replacement));
                    console.log(replacement);

            },
            failure: function(data) {
                alert('Got an error dude');
            }
        });


        //alert(str);
       //var replacement = 'apple';
       // $(this).html($(this).html().replace(str, replacement));

       });

      function fetchPoem(poem_id, poem_name) {
        document.getElementById("poemName").innerHTML = poem_name;
        document.getElementById("left_spinner").style.visibility = "visible";
        document.getElementById("poem").innerHTML = "";
        document.getElementById("actions").innerHTML = "";
        $.ajax({
          type: "POST",
          url: "./php/getpoem.php",
          data:{ poemID: poem_id, dest1: "originalText", dest2: "braileText" }, 
          success: function(data){ 
            var a = "<a href='javascript:printBraileText(\"braileText\");'>הדפסה</a> \\ <a href='javascript:makeTextFile(\"" +
            document.getElementById("poemName").innerHTML + "\",\"originalText\");'>שמירת טקסט עברי לקובץ</a> \\  <a href='javascript:makeBraileFile(\"" + 
            document.getElementById("poemName").innerHTML + "\",\"braileText\");'>שמירת טקסט ברייל לקובץ</a><br><br>";
            document.getElementById("actions").innerHTML= a;
            document.getElementById("poem").innerHTML = data;
            document.getElementById("left_spinner").style.visibility = "hidden";
            document.getElementById("poets").disabled = false;
            document.getElementById("poems").disabled = false; 

          }
        })
      }

      function fetchPoemTab2(poem_id, poem_name) {
        document.getElementById("poemNameTab2").innerHTML = poem_name;
        document.getElementById("left_spinner_tab2").style.visibility = "visible";
        document.getElementById("poem-tab2").innerHTML = "";
        document.getElementById("actions-tab2").innerHTML = "";

        $.ajax({
          type: "POST",
          url: "./php/getpoem.php",
          data:{ poemID: poem_id, dest1: "originalTextTab2", dest2: "braileTextTab2" }, 
          success: function(data){ 
            var a = "<a href='javascript:printBraileText(\"braileTextTab2\");'>הדפסה</a> \\ <a href='javascript:makeTextFile(\"" +
            document.getElementById("poemNameTab2").innerHTML + "\",\"originalTextTab2\");'>שמירת טקסט עברי לקובץ</a> \\  <a href='javascript:makeBraileFile(\"" + 
            document.getElementById("poemNameTab2").innerHTML + "\",\"braileTextTab2\");'>שמירת טקסט ברייל לקובץ</a><br><br>";
            document.getElementById("actions-tab2").innerHTML = a;
            document.getElementById("poem-tab2").innerHTML = data;
            document.getElementById("left_spinner_tab2").style.visibility = "hidden";

          }
        })
      }



      /////

      function fetchPoems() {
        document.getElementById("poem-tab2").innerHTML = ""; 
        document.getElementById("actions-tab2").innerHTML = "";  
        document.getElementById("poems-table-body-tab2").innerHTML = ""; 
        document.getElementById("spinner-tab2").style.visibility = "visible";
        

        $.ajax({
          type: "POST",
          url: "./php/getpoems.php",
          
          success: function(data){
            document.getElementById("poems-table-body-tab2").innerHTML = data;
            document.getElementById("spinner-tab2").style.visibility = "hidden";
            document.getElementById("spinnerTab4").style.visibility = "collapse";
            document.getElementById("stat").style.visibility = "visible";
            document.getElementById("autocomplete").placeholder = "";
            document.getElementById("autocomplete").disabled = false;
            var tags = $('#poems-table-body-tab2 > tr > td > a').toArray();



            document.getElementById("numOfPoems").innerHTML = tags.length;

            var poemsListStr = "";

            for (var i = 0, len = tags.length; i < len; i++) {
              var res = tags[i].toString().substring(25, tags[i].length);
              var resArr = res.split(",");
              var id = resArr[0];
              var name = resArr[1].substring(1,resArr[1].length-3).replace("  ", " ");
              tags[i] = {label: decodeURIComponent(name), value: id};
              poemsListStr += decodeURIComponent(name) + "\n";
            }

           document.getElementById("poemsList").innerHTML = poemsListStr;    


            $( "#autocomplete" ).autocomplete({
              source: tags,
                  select: function( event, ui ) { 
                      $( "#autocomplete" ).val(ui.item.label);
                      fetchPoemTab2(ui.item.value, ui.item.label);
                      event.preventDefault();
                  },
                  change: function( event, ui ) {
                      $( "#autocomplete" ).val(ui.item.label);
                      event.preventDefault();
                  },
                  focus: function( event, ui ) {
                      $( "#autocomplete" ).val(ui.item.label);
                      event.preventDefault();
                  },
                  function (array, term) {
                  var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(term), "i");
                  return $.grep(array, function (value) {
                      return matcher.test(value.label || value.value || value);
                  });
                },
                delay: 400,
          position: {
        my : "right top",
        at: "right bottom"
    }
            });




        $(function () {
            var _poems = $('#poems-table-body-tab2 > tr > td > a'); 

            _poems.click(function () {
              var _poem = $(this), _text = $(this).text(), _count = 0;
              _poems.removeClass("active");
              _poem.addClass("active");
              window.location.hash = "#" + "poems";



          });

        });

            $(function () {
              var _alphabets = $('.alphabet_poems_tab2 > a');
              var _contentRows = $('#poems-table-tab2 tbody tr');

              _alphabets.click(function () {
                var _letter = $(this), _text = $(this).text(), _count = 0;

                _alphabets.removeClass("active");
                _letter.addClass("active");

                _contentRows.hide();
                _contentRows.each(function (i) {
                  var _cellText = $(this).children('td').eq(0).text();
                  if (RegExp('^' + _text).test(_cellText)) {
                    _count += 1;
                    $(this).fadeIn(400);
                  }
                });
              });
            });

          }
        })
      }

      /////





      function fetchPoemsByPoet(poet_id) {
        document.getElementById("actions").innerHTML = "";
        document.getElementById("poem").innerHTML = ""; 
        document.getElementById("poems-table-body").innerHTML = ""; 

        document.getElementById("spinner").style.visibility = "visible";


        $.ajax({
          type: "POST",
          url: "./php/getpoemsbypoet.php",
          data:{ poetID: poet_id }, 
          success: function(data){
            document.getElementById("poems-table-body").innerHTML = data;
            document.getElementById("spinner").style.visibility = "hidden";


        $(function () {
            var _poets = $('#poems-table-body > tr > td > a'); 

            _poets.click(function () {
              var _poet = $(this), _text = $(this).text(), _count = 0;
              _poets.removeClass("active");
              _poet.addClass("active");



          });

        });

            $(function () {
              var _alphabets = $('.alphabet_poems > a');
              var _contentRows = $('#poems-table tbody tr');

              _alphabets.click(function () {
                var _letter = $(this), _text = $(this).text(), _count = 0;

                _alphabets.removeClass("active");
                _letter.addClass("active");

                _contentRows.hide();
                _contentRows.each(function (i) {
                  var _cellText = $(this).children('td').eq(0).text();
                  if (RegExp('^' + _text).test(_cellText)) {
                    _count += 1;
                    $(this).fadeIn(400);
                  }
                });
              });
            });

          }
        })
      }

      var poets = [];

      function fetchPoets() {
        document.getElementById("spinner").style.visibility = "visible";

    //above (HotelArea) are actually the value (this.value) in the form which will be what the user select (North, South, East or West)
    var xhttp = new XMLHttpRequest();
    var url = "./php/getpoets.php";//<- just a sample url
    var data = new FormData();
    //below will "assign HotelArea to $_POST['SearchValue']"
    //data.append('SearchValue',HotelArea);
    xhttp.open('POST',url,true);
    xhttp.setRequestHeader("Content-Type", "text/plain;charset=UTF-8"); 
    xhttp.send(data);
    
    xhttp.onreadystatechange = function() { 
      if(xhttp.readyState == 4 && xhttp.status == 200) {  
        document.getElementById("poets-table-body").innerHTML = xhttp.responseText;
        document.getElementById("spinner").style.visibility = "hidden";

        $(function () {
            var _poets = $('#poets-table-body > tr > td > a'); 
            var _alphabets_poems = $('.alphabet_poems > a');    

            _poets.click(function () {
              var _poet = $(this), _text = $(this).text(), _count = 0;
              _poets.removeClass("active");
              _alphabets_poems.removeClass("active");
              _poet.addClass("active");


          });

        });

        $(function () {
          var _alphabets = $('.alphabet > a');
          var _contentRows = $('#poets-table tbody tr');

          _alphabets.click(function () {
            var _letter = $(this), _text = $(this).text(), _count = 0;

            _alphabets.removeClass("active");
            _letter.addClass("active");

            _contentRows.hide();
            _contentRows.each(function (i) {
              var _cellText = $(this).children('td').eq(0).text();
              if (RegExp('^' + _text).test(_cellText)) {
                _count += 1;
                $(this).fadeIn(400);
              }
            });



          });

        });


        var i = 0;
        var poetsListStr = "";
         $('#poets-table-body > tr > td > a').each( function(){
              line = $(this).text();
              if(line[line.length-1] == ')'){ 
                lastP = line.lastIndexOf("(");
                name = line.substring(0,lastP-1);
                date = line.substring(lastP+1,line.length-1);
                dateParts = date.split("-");
                dateOfBirth = dateParts[0];
                dateOfDeath = dateParts[1];
                poets.push({ term: i.toString(), name: name, birthDate: new Date(parseInt(dateOfBirth), 1, 1), deathDate: new Date(parseInt(dateOfDeath), 1, 1) });
                poetsListStr += name + "\n";
                i +=1;
              }
          });

         document.getElementById("numOfPoets").innerHTML = poets.length; 
         document.getElementById("poetsList").innerHTML = poetsListStr;    
   

      }       
    }   
  }

  var chartLoaded = 0;
  function drawChart() {
    var container = document.getElementById('example2.1');
    var chart = new google.visualization.Timeline(container);
    container.width = 300;
    var dataTable = new google.visualization.DataTable();

    dataTable.addColumn({ type: 'string', id: 'Term' });
    dataTable.addColumn({ type: 'string', id: 'Name' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });

    poets.forEach(function(poet) {
       dataTable.addRow([  poet.term, poet.name, poet.birthDate, poet.deathDate ]);
    });

    chart.draw(dataTable);
  }


  function onLoad(){
      fetchPoets();
      fetchPoems();

      /*document.getElementById("tl").onclick = function(){
        if(chartLoaded == 0){
            setTimeout(function() {
            if(poets.length == 0){
              setTimeout(function(){
                google.charts.load("current", {packages:["timeline"]});
                google.charts.setOnLoadCallback(drawChart);
              },4000);
            }
            else{
              google.charts.load("current", {packages:["timeline"]});
              google.charts.setOnLoadCallback(drawChart);
            }
            chartLoaded = 1;
          }, 1000);          
        }
      };*/

  }

  window.onload = onLoad;


  function printBraileText(textSource) {
    childWindow = window.open('','childWindow','location=yes, menubar=yes, toolbar=yes');
    childWindow.document.open();
    childWindow.document.write('<html><head></head><body>');
    childWindow.document.write(document.getElementById(textSource).innerHTML.replace(/\n/gi,'<br>'));
    childWindow.document.write('</body></html>');
    childWindow.print();
    childWindow.document.close();
    childWindow.close();
  }



  function makeTextFile(poemName,textSource) {

    data = new Blob([
  new Uint8Array([0xEF, 0xBB, 0xBF]), // UTF-8 BOM
  document.getElementById(textSource).innerHTML.replace(/\n/g, "\r\n").replace(/&nbsp;/g, ' ')

  ],
  { type: "text/plain;charset=utf-8" });



    var a = document.createElement("a"),
    url = URL.createObjectURL(data);
    a.href = url;
    a.download = poemName + "-hebrew.txt";
    document.body.appendChild(a);
    a.click();
    setTimeout(function() {
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);  
    }, 0); 
  }

  function makeBraileFile(poemName, textSource) {

    data = new Blob([
  new Uint8Array([0xEF, 0xBB, 0xBF]), // UTF-8 BOM
  document.getElementById(textSource).innerHTML.replace(/\n/g, "\r\n")

  ],
  { type: "text/plain;charset=utf-8" });



    var a = document.createElement("a"),
    url = URL.createObjectURL(data);
    a.href = url;
    a.download = poemName + "-braile.txt";
    document.body.appendChild(a);
    a.click();
    setTimeout(function() {
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);  
    }, 0); 
  }

  function downloadList(src) {

    data = new Blob([
  new Uint8Array([0xEF, 0xBB, 0xBF]), // UTF-8 BOM
  document.getElementById(src).innerHTML.replace(/\n/g, "\r\n").replace(/&nbsp;/g, ' ')

  ],
  { type: "text/plain;charset=utf-8" });

    var a = document.createElement("a"),
    url = URL.createObjectURL(data);
    a.href = url;
    a.download = generateUID() + ".txt";
    document.body.appendChild(a);
    a.click();
    setTimeout(function() {
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);  
    }, 0); 
  }


function generateUID() {
    // I generate the UID from two parts here 
    // to ensure the random number provide enough bits.
    var firstPart = (Math.random() * 46656) | 0;
    var secondPart = (Math.random() * 46656) | 0;
    firstPart = ("000" + firstPart.toString(36)).slice(-3);
    secondPart = ("000" + secondPart.toString(36)).slice(-3);
    return firstPart + secondPart;
}



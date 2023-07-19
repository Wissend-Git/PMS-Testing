$.fn.dataTable.Api.register('column().searchable()', function() {
  var ctx = this.context[0];
  return ctx.aoColumns[this[0]].bSearchable;
});

$(document).ready(function() {
  var table = $('#ms_table').DataTable({
      fixedHeader: true,
      pageLength: 10,
      "lengthMenu": [[10, 25, 50, -1],[10,25,50,"All"]],
      orderCellsTop: true,
      "order": [ 3, 'asc' ],
      "order": [ 0, 'asc' ],
      "footerCallback": function () { }
  } );

  table.columns().every(function() {
    if (this.searchable()) {
        var that = this;
        var myList = $('<ul/>');
        var myMulti = $('<div class="mutliSelect"/>');
        myList.appendTo(myMulti);
        var myDd = $('<dd/>');
        myMulti.appendTo(myDd);
  
        var myDropdown = $('<dl class="dropdown"/>');
        myDropdown.append('<dt><a><span class="hida">Select</span></a></dt>');
        myDd.appendTo(myDropdown);
        myDropdown.appendTo($('thead tr:eq(1) td').eq(this.index())).on('change', function() {
            var vals = $(':checked', this).map(function(index, element) {
              return $.fn.dataTable.util.escapeRegex($(element).val());
            }).toArray().join('|');
          that.search(vals.length > 0 ? '^(' + vals + ')$' : '', true, false).draw();
        });
        
        $cb_3 = $('<span id="btnsel" class="col-md-6">SelectAll</span>');
        $cb_4 = $('<span id="btncl" class="col-md-6">ClearAll</span>');
        myList.append($('<li>').append($cb_3).append($cb_4));
        $('#btnsel', $('thead tr:eq(1) td').eq(this.index())).on('click', function(){
            $('input[type=checkbox]').prop('checked', true);
            that.data().each(function(a){
                that.search(a.length > 0 ? '' : '^(' + a + ')$', false, true).draw();
            });
          });
        $('#btncl', $('thead tr:eq(1) td').eq(this.index())).on('click', function(){
            $('input[type=checkbox]').prop('checked', false);
            that.data().each(function(a){
                that.search(a.length > 0 ? '' : '^(' + a + ')$', false, true).draw();
            });
        });
        this.data().sort().unique().each(function(d) {
          let travel = that.index()+1
          myList.append($('<li><input type="checkbox" class ="it" id = '+d+' value="' + d + '"/><label for = '+d+'>'+d+'</label></option>'));
          // myList.append($('<li><input type="checkbox" id = '+d[0]+'_'+travel.toString()+' value="' + d + '"/><label for = '+d[0]+'_'+travel.toString()+'>'+d+'</label></option>'));
        });
    }
  });
  
  $(".dropdown dt a").on('click', function(e) {
    var dropdown = $(this).closest('.dropdown');
    dropdown.find('ul').slideToggle('fast');
    $('.dropdown').not(dropdown).find('ul').slideUp('fast');
  });

  $(document).bind('click', function(e) {
      var $clicked = $(e.target);
      if (!$clicked.parents().hasClass("dropdown")) $(".dropdown dd ul").slideUp('fast');
  });
});
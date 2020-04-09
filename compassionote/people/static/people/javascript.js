function select_all(source) 
{
    checkboxes = document.getElementsByName('contactKey');
    for(var i=0, n=checkboxes.length; i<n; i++) 
    {
        checkboxes[i].checked = source.checked;
    }
}

$('select#match').change(function(){

    theVal = $(this).children(':selected').text();
    $('span.date').each(function(){

        if($(this).text()==theVal){
            $('li.pr').hide();
            $(this).parent().show();
        }
    });
});

$(function () 
{
    var $matchFilter = $('select[name=matchFilter]');
    $matchFilter.change(function () 
    {
        var $selectedValue = $(this).find('option:selected').val();
        console.log($selectedValue);
        if($selectedValue == 1)
        {
            $( "tr#matched_person td#matched" ).each(function( ) 
            {
                if($(this).find("[value]").val() == "Match")
                {
                    $(this).parent().hide();
                }
            });
        }
        if($selectedValue == 2)
        {
            $( "tr#matched_person td#matched" ).each(function( ) 
            {
                $(this).parent().show();
            });
        }
    });
});


$( document ).ready(function() 
{
    $( "#filter" ).click(function() 
    {
        var filter = $( "input[name=filterValue]" ).val();
        console.log("Hello");
        console.log(filter);
        $( "tr #matched_person" ).each(function( i ) 
        {
            $(this).hide();
        });
    });
});
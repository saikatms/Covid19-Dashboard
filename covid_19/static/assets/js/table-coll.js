    $(document).ready(function() {
    $('tr.category').on('click', function() {
       $(this).nextUntil('.category').fadeToggle();
    });
});
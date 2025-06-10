$(document).ready(function(){
    $('#total_amount').inputmask('decimal', {
        alias: 'numeric',
        groupSeparator: '.',
        autoGroup: true,
        digits: 2,
        digitsOptional: false,
        prefix: 'R$ ',
        placeholder: '0',
        rightAlign: false,
        autoUnmask: true
    });
});
$(document).ready(function () {
    $('[data-toggle="offcanvas"]').click(function () {
        $('.row-offcanvas').toggleClass('active')
    });
    check_all_click();
});

function check_all_click() {
    // 全选函数
    $("input[type='checkbox'][data-check-all='true']").on('click', function () {
        $(this).parents("table").find("input[type='checkbox'][data-check-all!='true']").click();
    });
}
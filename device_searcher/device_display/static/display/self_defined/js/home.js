// 给String对象加上一个去掉前后空格的函数
String.prototype.Trim = function () {
    return this.replace(/(^\s*)|(\s*$)/g, "");
};

// 给全选checkbox绑定点击事件,点击全选
function check_all_click() {
    $("input[type='checkbox'][data-check-all='true']").on('click', function () {
        $(this).parents("table").find("input[type='checkbox'][data-check-all!='true']").click();
    });
}

$(document).ready(function () {
    // 控制最顶端的导航栏的激活跳转,即调整当前的active的项
    $('[data-toggle="offcanvas"]').click(function () {
        $('.row-offcanvas').toggleClass('active')
    });

    // 构造退出和登录按钮的跳转链接
    // 将当前页面的链接传入登录退出的href，以便登录和退出成功后跳转回来
    var next_href = window.location.href;
    var url_logout = get_url("display:logout");
    var url_login = get_url("display:getPage_signin");
    url_logout = url_logout.concat("?next=", next_href);
    url_login = url_login.concat("?next=", next_href);

    $("#bt_logout").attr("href", url_logout);
    $("#bt_login").attr("href", url_login);

    // 给所有的全选checkbox加上点击全选事件
    check_all_click();

});


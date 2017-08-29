/**
 * Created by wycheng on 8/29/17.
 */

//设置导航栏的元素active切换
$(document).ready(function () {
    $("li.nav_li").attr("class", "nav_li");
    $("li#nav_search").addClass("active");
});

//提交表单函数
function tosubmit(category) {
    var search_category = $("input#search_category");
    search_category.val(category);
    $("button#btn_submit").click();
}
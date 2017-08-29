/**
 * Created by wycheng on 8/29/17.
 */
// 点击页码后会调用的函数
function after_click_page() {
    var page_index = $("input[name= 'input_page_index']").val();
    get_manage_logs(page_index);
}

$(document).ready(
    function () {
        //设置导航栏的元素active切换
        $("li.nav_li").attr("class", "nav_li");
        $("li#nav_log").addClass("active");

        var input_page_total = $("input[name= 'input_page_total']");
        var input_page_index = $("input[name= 'input_page_index']");

        // 按当前页码（默认为1）调用获取日志的函数
        get_manage_logs(input_page_index.val());

        // 按当前页码和页码总数调整页码组件,并传入点击页码后需要调用的函数
        adjust_pages(input_page_total, input_page_index, after_click_page);
    }
);

// 获取日志并显示的函数
function get_manage_logs(page_index) {
    var tbody = $("table tbody");
    var url_get_logs = get_url("display:get_manage_log");
    $.get(url_get_logs,
        {"page_index": page_index},
        function (data, status) {
            if (status === "success") {
                tbody.empty();
                var result_json = eval('(' + data + ')');
                for (log_ind in result_json) {
                    var log = $('<tr>' +
                        '<td>' + result_json[log_ind].opt_time + '</td>' +
                        '<td>' + result_json[log_ind].opt_user + '</td>' +
                        '<td>' + result_json[log_ind].opt_brief + '<a href="#" data-toggle="tooltip" title="' + result_json[log_ind].opt_detail + '">（查看详情请悬停在我上面）</a></td>' +
                        '</tr>');

                    tbody.append(log);
                }
            } else {
                Messenger().post("获取log请求失败了");
            }
        });

}
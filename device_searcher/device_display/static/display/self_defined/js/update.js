/**
 * Created by wycheng on 8/29/17.
 */

$(document).ready(
    function () {
        $("li.nav_li").attr("class", "nav_li");
        $("li#nav_update").addClass("active");

        var nav_text = $("input#nav_text").val();
        if (nav_text === "updfile_success") {
            Messenger().post("文件导入完毕");
            $('a[href = "#panel_upload"]').click();
        }

        // 初始化源网站列表
        init_website_list();

        // 给从网站爬取更新的立即更新按钮添加点击事件
        update_immediately_click();

        // 初始化更新日志列表
        init_updrcd_list();

        // 添加上传文件的点击事件
        btn_uploader_browse_click();

        // 导入文件的点击事件
        btn_uploader_start_click();
    }
);
function btn_uploader_start_click() {
    $("button#uploader_start").on("click", function () {
            var num_tr = $("form.form_upl_files tbody").find("tr").length;
            if (num_tr <= 0) {
                alert("没有添加任何文件");
            } else {
                var btns_upl_file = $("button.btn_upl_file");
                btns_upl_file.click();
            }
        });
}
function btn_uploader_browse_click() {
    $("button#uploader_browse").on("click", function () {
            var tbody = $("form.form_upl_files tbody");

            var num_tr = tbody.find("tr").length;

            var tr_upl_file = $('<tr>' +
                '<td class="checkbox_par">' +
                '<input type="checkbox">' +
                '</td>' +
                '<td>' +
                '<input type="file" name="upl_file_' + num_tr + '">' +
                '</td>' +
                '</tr>');

            tbody.append(tr_upl_file);// 在tbody中添加一行

            tr_upl_file.find("input").click();// 新增一条后立即点击浏览进行文件选择
        });
}

function init_updrcd_list() {
    var url_updrcd = get_url("display:get_updrcd_list");
        $.get(url_updrcd,
            {"page": "1"},
            function (data, status) {
                if (status === "success") {
                    var tbody = $("div#panel_upd_rcd table tbody");
                    tbody.empty();
                    var result_json = eval('(' + data + ')');
                    for (rcd_ind in result_json) {
                        add_row_upd_rcd(parseInt(rcd_ind) + 1, result_json[rcd_ind].id,
                            result_json[rcd_ind].data_src_name, result_json[rcd_ind].upd_time,
                            result_json[rcd_ind].type_num, result_json[rcd_ind].brand_num, result_json[rcd_ind].model_num);
                    }
                } else {
                    Messenger().post("获取更新日志列表请求失败了");
                }
            });
}

function init_website_list() {
    var url_website = get_url("display:get_srcweb_list");
    $.get(url_website,
        function (data, status) {
            if (status === "success") {
                var tbody = $("div#panel_crawl table tbody");
                tbody.empty();
                var result_json = eval('(' + data + ')');
                for (web_ind in result_json) {
                    add_row_crawl(parseInt(web_ind) + 1, result_json[web_ind].id,
                        result_json[web_ind].name, result_json[web_ind].website, result_json[web_ind].cycle);
                }

                // 给源网站下拉框添加选择变更事件
                on_adjust_circle();
            } else {
                Messenger().post("获取源网站列表请求失败了");
            }
        });
}

// 添加一条源网站表格行
function add_row_crawl(serial_num, web_id, web_name, website, cycle) {
    var tbody = $("div#panel_crawl table tbody");
    var row = $('<tr data-website-id="' + web_id + '">' +
        '<td class="checkbox_par">' +
        '<input type="checkbox">' +
        '</td>' +
        '<td>' + serial_num + '</td>' +
        '<td><a target="_blank" href="' + website + '">' + web_name + '</a></td>' +
        '<td>' +
        '<select class="selectpicker show-tick form-control" name="circle"' +
        'data-width="98%" data-first-option="false" required>' +
        '<option value="1">1个月</option>' +
        '<option value="2">2个月</option>' +
        '<option value="3">3个月</option>' +
        '<option value="6">6个月</option>' +
        '<option value="12">1年</option>' +
        '</select>' +
        '</td>' +
        '</tr>');


    tbody.append(row);
    // select2动态加元素需要刷新
    var circle_sp = row.find("select.selectpicker");
    circle_sp.selectpicker('render');
    circle_sp.selectpicker("refresh");

    circle_sp.selectpicker('val', cycle);// 设置默认选项
}

// 增加一行文件（上传）导入表格行
function add_row_upload(serial_num, file_name, file_path, category) {
    var tbody = $("div#panel_upload table tbody");
    var row = $('<tr>' +
        '<td>' +
        '<input type="checkbox" data-file-path=' + file_path + '>' +
        '</td>' +
        '<td>' + serial_num + '</td>' +
        '<td> + file_name + </td>' +
        '<td> + category + </td>' +
        '</tr>');

    tbody.append(row);
}

// 新增一条更新记录表格行
function add_row_upd_rcd(serial_num, upd_rcd_id, data_src, upd_time, type_num, brand_num, model_num) {
    var tbody = $("div#panel_upd_rcd table tbody");
    var row = $('<tr data-updrcd-id="' + upd_rcd_id + '">' +
        '<td>' + serial_num + '</td>' +
        '<td>' + data_src + '</td>' +
        '<td>' + upd_time + '</td>' +
        '<td>' + type_num + '</td>' +
        '<td>' + brand_num + '</td>' +
        '<td>' + model_num + '</td>' +
        '</tr>');

    tbody.append(row);
}

// 给源网站更新周期的下拉框添加选择改变事件
function on_adjust_circle() {
    var circle_select = $("select.selectpicker[name = 'circle']");
    circle_select.on("changed.bs.select", function () {
        var new_circle = $(this).selectpicker("val");
        var web_id = $(this).parents("tr").data("websiteId");

        var url_adj_circle = get_url("display:adjust_upd_circle");
        $.post(url_adj_circle,
            {
                "new_circle": new_circle,
                "web_id": web_id
            },
            function (data, status) {
                if (status === "success") {
                    Messenger().post("调整周期请求成功");
                } else {
                    Messenger().post("调整周期请求失败");
                }
            });
    });
}

// 立即从选中的源网站中爬取更新的数据
function update_immediately_click() {
    $('button#update_immediately').on('click', function () {
        var id_list = [];
        var count = 0;
        var checkedboxes = $("div#panel_crawl input[type='checkbox']:checked");
        checkedboxes.each(function (index, data) {
            var website_id = $(this).parents('tr').data('websiteId');
            if (typeof(website_id) !== "undefined") {// 过滤掉选中的全选checkbox
                id_list[count++] = website_id;
            }
        });

        var url_upd_immediately = get_url("display:update_immediately");

        $.post(url_upd_immediately,
            {"website_id_list": JSON.stringify(id_list)},
            function (data, status) {
                if (status === "success") {
                    Messenger().post("立即更新请求成功");
                } else {
                    Messenger().post("立即更新请求失败");
                }
            });
    });
}

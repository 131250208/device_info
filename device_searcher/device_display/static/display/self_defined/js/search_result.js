/**
 * Created by wycheng on 7/25/17.
 */
<!--初始化翻页组件和分类tab组件，并为之注册点击事件-->
$(document).ready(
    function () {
        // 注册点击分类tab的事件
        cat_tab_click();

        // 显示搜索结果
        get_results_post();

        // 初始化翻页组件并设置当前页码标签设为active
        var input_page_total = $("input#page_total");
        var input_page_index = $("input[name='page_index']");
        adjust_pages(input_page_total, input_page_index, get_results_post);

        // 为搜索按钮注册点击事件。
        $("button#btn_search").click(function () {
            get_results_post();
        });

        // 为[添加]按钮添加点击事件
        bt_add_click();

        // 给【确定添加】按钮添加点击事件
        bt_confirm_to_add_click();

        // 为删除按钮添加点击事件
        bt_delete_click();

        // 为修改按钮注册点击事件
        bt_edit_click();

        // 为导出按钮添加点击事件
        bt_export_click();

        // 为下拉框添加选择事件
        select_changed();

        // 调整结果容器的高
        var height = window.innerHeight - 380;
        $('div.results_content').css("min-height", height);

    }
);

function append_tr(father, row, relevancy_sign) {
    var unit = "td";
    if (row.id === -1) {
        unit = "th"
    }
    var tr = document.createElement("tr");

    // 先构造第一个包含复选框的td/th
    var check_box = document.createElement("input");
    check_box.type = "checkbox";
    check_box.value = row.id;

    var chk_box_inp = document.createElement(unit);
    chk_box_inp.className = "col-sm-1 checkbox_par";
    chk_box_inp.appendChild(check_box);

    if (row.id === -1) {
        check_box.style.marginRight = "5px";
        check_box.dataset.checkAll = "true";
        chk_box_inp.append('全选');
    }

    tr.appendChild(chk_box_inp);

    // 遍历构造包含每个字段对应值的td并添加到tr中
    var val_list = row.field_val;
    for (var i = 0; i < val_list.length; ++i) {
        var th = document.createElement(unit);
        th.dataset.relevancy = relevancy_sign[i];
        if (relevancy_sign[i] != "none" && row.id !== -1) {// 关联字段且非标题行加带有onclick的a标签
            var text = '"' + val_list[i] +'"';
            var category = '"' + relevancy_sign[i] +'"';

            // 加上点击搜索函数，和悬停显示关联记录
            th.innerHTML = "<a href='#' data-toggle='tooltip' title='"+ row.detail_list[i] +"' " +
                "onclick='relevancy_click(" + text + "," + category + ")'>" + val_list[i] + "</a>";
        }else {
            th.innerHTML = val_list[i];
        }
        tr.appendChild(th);
    }
    father.append(tr);
}

// 关联字段点击查找
function relevancy_click(search_text, search_category) {
    var inp_search_text = $("input[name='search_text']");
    var inp_page_index = $("input[name='page_index']");
    inp_search_text.val(search_text);
    inp_page_index.val("1");

    // 移除当前tab的active类
    $('#nav_result_cat').children().removeClass('active');

    switch (search_category) {
        case "category":
            $("li.cat#cat_category").addClass('active').click();
            break;
        case "type":
            $("li.cat#cat_type").addClass('active').click();
            break;
        case "brand":
            $("li.cat#cat_brand").addClass('active').click();
            break;
        case "model":
            $("li.cat#cat_model").addClass('active').click();
            break;
        case "fingerprint":
            $("li.cat#cat_fingerprint").addClass('active').click();
            break;
    }
}

// 将查询结果显示到表格上
function show_intable(result_json) {
    // result_info
    var info = $('p#result_info');
    info.html("查找结果：" + result_json.records_num + " 条&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;共 " + result_json.page_total + " 页&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;耗时：" + result_json.search_time + " s");
    $("input#page_total").val(result_json.page_total);

    var relevancy_sign = result_json.relevancy;
    // thead
    var thead = $('table.table thead');
    thead.empty();

    var field_names = result_json.fieldnames;
    var thead_dict = {'id': -1, 'field_val': field_names};

    append_tr(thead, thead_dict, relevancy_sign);

    // tbody
    var tbody = $("table.table tbody");
    tbody.empty();

    var list = result_json.record_list;
    for (var j = 0; j < list.length; ++j) {
        append_tr(tbody, list[j], relevancy_sign);
    }

    check_all_click();
}

// 注册点击分类tab的事件,将对应的分类作为参数放到隐藏的input里
function cat_tab_click() {
    $('.cat').click(function () {
        var inp_searchcat = $('input#searchcat');
        switch ($(this).attr('id')) {
            case 'cat_category' :
                inp_searchcat.val('category');
                break;
            case 'cat_type' :
                inp_searchcat.val('type');
                break;
            case 'cat_brand' :
                inp_searchcat.val('brand');
                break;
            case 'cat_model' :
                inp_searchcat.val('model');
                break;
            case 'cat_fingerprint' :
                inp_searchcat.val('fingerprint');
                break;
        }

        // 将添加编辑框收起
        $("button#btn_add").html("<span class='glyphicon glyphicon-chevron-down'></span> 添加");// 还原成添加按钮

        var input_text = $("div#add_editor form div.container input[type = 'text']");// 清空input
        input_text.val("");

        $("div.collapse").collapse("hide");// 收起编辑框

        // 发送搜索请求
        get_results_post();
    });
}

// 搜索结果的接口的调用函数
function get_results_post() {
    var inp_search_text = $("input[name='search_text']");
    var search_text = inp_search_text.val();

    var search_category = $("input[name='search_category']").val();
    var page_index = $("input[name='page_index']").val();
    // 发送post请求调用接口
    if (search_text === "") {
        search_text = $('input#searchtext_last').val();
        inp_search_text.val(search_text);
    }
    get_results(search_text, search_category, page_index);
}

// 返回选中的元组id，如果没有选中项则返回空数组
function get_ids_checked() {
    var id_list = [];
    var count = 0;
    var checkedboxes = $("input[type='checkbox']:checked");
    checkedboxes.each(function (index, data) {
        if (data['value'] != -1) {
            id_list[count++] = data['value'];
        }
    });
    return id_list;
}
// 给[添加]添加点击事件
function bt_add_click() {
    $("button#btn_add").on("click", function () {
        var edit_category = $("input[name='search_category']").val();

        var input_edit_category = $("div#add_editor form input[name = 'edit_category']");
        input_edit_category.val(edit_category);

        var btn_str = $(this).text().Trim();
        if (btn_str === "添加") {
            // 切换图标
            $(this).html("<span class='glyphicon glyphicon-chevron-up'></span> 收起");

            $("#" + "add_editor_" + edit_category).collapse("show");
        } else {
            // 切换图标
            $(this).html("<span class='glyphicon glyphicon-chevron-down'></span> 添加");
            var input_text = $("div#add_editor form div.container input[type = 'text']");
            input_text.val("");

            $("#" + "add_editor_" + edit_category).collapse("hide");
        }
    });
}

// 给【确定添加】按钮添加点击事件
function bt_confirm_to_add_click() {
    $("button.confirm_add").on("click", function () {
        var thisform = $(this).parents("form");
        var add_category = $("input[name = 'search_category']").val();

        var record = null;
        var record_str = "";

        switch (add_category) {
            case "category":
                var category = thisform.find("input[name = 'category']").val();
                var category_cn_name = thisform.find("input[name = 'category_cn_name']").val();
                var category_en_name = thisform.find("input[name = 'category_en_name']").val();
                var description = thisform.find("textarea[name = 'description']").val();

                record = {
                    "category": category,
                    "cn_name": category_cn_name,
                    "en_name": category_en_name,
                    "description": description,
                };

                record_str = JSON.stringify(record);
                break;
            case "type":
                var type = thisform.find("input[name = 'type']").val();
                var type_cn_name = thisform.find("input[name = 'type_cn_name']").val();
                var type_en_name = thisform.find("input[name = 'type_en_name']").val();
                var category = thisform.find("select[name = 'category']").val();
                var description = thisform.find("textarea[name = 'description']").val();

                record = {
                    "type": type,
                    "type_cn_name": type_cn_name,
                    "type_en_name": type_en_name,
                    "category": category,
                    "description": description,
                };

                record_str = JSON.stringify(record);
                break;
            case "brand":
                var brand_cn_name = thisform.find("input[name = 'brand_cn_name']").val();
                var brand_en_name = thisform.find("input[name = 'brand_en_name']").val();
                var country = thisform.find("select[name = 'country']").val();
                var product_type = thisform.find("select[name = 'type']").val();
                var brand_link = thisform.find("input[name = 'brand_link']").val();
                var description = thisform.find("textarea[name = 'description']").val();

                record = {
                    "cn_name": brand_cn_name,
                    "en_name": brand_en_name,
                    "country": country,
                    "product_type": product_type,
                    "brand_link": brand_link,
                    "description": description
                };

                record_str = JSON.stringify(record);
                break;
            case "model":
                var model = thisform.find("input[name = 'model']").val();
                var model_link = thisform.find("input[name = 'model_link']").val();
                var type = thisform.find("select[name = 'type']").val();
                var category = thisform.find("select[name = 'category']").val();
                var brand = thisform.find("select[name = 'brand']").val();
                var description = thisform.find("textarea[name = 'description']").val();

                record = {
                    "model": model,
                    "model_link": model_link,
                    "type": type,
                    "category": category,
                    "brand": brand,
                    "description": description
                };

                record_str = JSON.stringify(record);
                break;
            case "fingerprint":
                var accuracy = thisform.find("input[name = 'accuracy']").val();
                var match_type = thisform.find("select[name = 'match_type']").val();
                var protocol = thisform.find("input[name = 'protocol']").val();
                var category = thisform.find("select[name = 'category']").val();
                var type = thisform.find("select[name = 'type']").val();
                var brand = thisform.find("select[name = 'brand']").val();
                var model = thisform.find("select[name = 'model']").val();
                var server = thisform.find("input[name = 'server']").val();
                var www_authenticate = thisform.find("input[name = 'www_authenticate']").val();
                var title = thisform.find("input[name = 'title']").val();
                var others = thisform.find("input[name = 'others']").val();

                record = {
                    "accuracy": accuracy,
                    "match_type": match_type,
                    "protocol": protocol,
                    "device_category": category,
                    "device_type": type,
                    "brand": brand,
                    "model": model,
                    "server": server,
                    "www_authenticate": www_authenticate,
                    "title": title,
                    "others": others
                };

                record_str = JSON.stringify(record);
                break;
        }

        add_record(add_category, record_str);
    });
}

// 给删除按钮注册点击事件
function bt_delete_click() {
    $('button#btn_delete').on('click', function () {
        var delete_id_list = get_ids_checked();
        if (delete_id_list.length != 0) {
            var delete_category = $("input[name='search_category']").val();
            delete_row(delete_id_list, delete_category);
        } else {
            //
            alert("没有选中任何项");
        }
    });
}

// 给修改按钮添加点击事件
function bt_edit_click() {
    $('button#btn_edit').on('click', function () {
        var str = $(this).text().Trim();

        if (str === "修改") {
            var checked_boxes = $("input[type='checkbox']:checked");

            if (checked_boxes.length <= 0) {// 先检验是否有选中项
                alert("你没有选中任何项");
            }
            else {
                // 切换图标
                $(this).html("<span class='glyphicon glyphicon-floppy-save'></span> 保存");
                // 将表格切换成编辑框
                checked_boxes.parent().siblings("td").each(function () {
                    var text_inputs = $(this).find("input:text");// 验证是否存在编辑框
                    var relevancy = $(this).data("relevancy");

                    if (!text_inputs.length && relevancy === "none") { // 如果不存在编辑框且为非关联字段,关联字段暂定不可修改
                        // 用 data-text-before 属性来保存原来的值，以便修改失败后恢复显示
                        $(this).html("<input type='text' class='form-control_self' " +
                            "data-text-before='" + $(this).text() + "' style='background-color: transparent' value='" + $(this).text() + "'>");

                    }
                });
            }


            // alert($("tbody tr:nth-of-type(2n)").css("color"));
        }
        else if (str === "保存") {
            // 切换图标
            $(this).html("<span class='glyphicon glyphicon-pencil'></span> 修改");

            var checked_boxes = $("input[type='checkbox']:checked");
            if (checked_boxes.length > 0) {
                var row_list = [];// 用于存放待修改的元组数据
                var count_edit = 0;

                checked_boxes.each(function () {
                    var text_inputs = $(this).parent().siblings().find("input:text");
                    if (text_inputs.length > 0) {// 用于判断选中项是否可编辑，不可编辑则无效
                        var checked_row = [];
                        checked_row[0] = $(this).val();
                        $(this).parent().siblings().each(function (index, element) {
                            checked_row[index + 1] = $(this).children("input").val();
                        });
                        row_list[count_edit++] = checked_row;
                    }
                });
                // alert(edit_list.join(";"));

                // 先将编辑框取消
                $("tbody td input:text").each(function () {
                    $(this).parent().html($(this).data("textBefore"));// 回复data-text-before里存储的值
                });

                // 调用修改接口
                if (count_edit === 0) {
                    alert("没有选中任何有效选项");
                } else {
                    var edit_category = $("input[name='search_category']").val();
                    edit_row(row_list, edit_category);
                }
            } else {
                // 将编辑框取消
                $("tbody td input:text").each(function () {
                    $(this).parent().html($(this).data("textBefore"));// 回复name里存储的值
                });
                alert("没有选中任何项");
            }
        }
    });
}





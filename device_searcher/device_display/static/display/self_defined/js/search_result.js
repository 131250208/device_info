/**
 * Created by wycheng on 7/25/17.
 */


function append_tr(father, row) {
    var unit = "td"
    if (row.id === -1) {
        unit = "th"
    }
    var tr = document.createElement("tr");

    var input = document.createElement("input");
    input.type = "checkbox";
    input.value = row.id;
    var chk_box = document.createElement(unit);
    chk_box.appendChild(input);

    if (row.id === -1) {
        input.style.marginRight = "5px";
        chk_box.append('全选');
    }

    tr.appendChild(chk_box);

    var val_list = row.field_val;
    for (var i = 0; i < val_list.length; ++i) {
        var th = document.createElement(unit);
        th.innerHTML = val_list[i];
        tr.appendChild(th);
    }
    father.append(tr);
}

// 将查询结果显示到表格上
function show_intable(result_json) {
    // thead
    var thead = $('table.table thead');
    thead.empty();

    var field_name = {'id': -1, 'field_val': ['field_name1', 'field_name2', 'field_name3', 'field_name4']}
    // var result_json = eval('(' + data + ')');
    append_tr(thead, field_name)

    // tbody
    var tbody = $("table.table tbody");
    tbody.empty();

    var list = result_json.record_list;
    for (var j = 0; j < list.length; ++j) {
        append_tr(tbody, list[j]);
    }

    //
    check_all_click();
}

// 根据当前页码调整翻页组件,当前页码标签设为active
// 该调整函数会将原来的页码元素清空，所以需要重新注册点击事件
function adjust_pages() {
    var page_index = $("input[name='page_index']").val();

    var pagination = $('ul.pagination');
    pagination.empty();

    var page_current_li = page_li(page_index);
    pagination.append(page_current_li);
    page_current_li.addClass('active');

    var bf_num = 4;
    var aft_num = 5;

    var page_num_bf = parseInt(page_index);
    while (bf_num) {
        if (--page_num_bf <= 0) {
            break;
        }
        bf_num--;
        pagination.prepend(page_li(String(page_num_bf)));
    }
    aft_num += bf_num;// 如果前方待插入数还有余，用于后方插入直到遇到末页

    var page_end = $("input#page_total").val();
    var page_num_aft = parseInt(page_index);
    while (aft_num) {
        if (++page_num_aft > page_end) {
            break;
        }
        aft_num--;
        pagination.append(page_li(String(page_num_aft)));
    }

    if (aft_num) {// 如果后方待插入数还有余，用于前方插入直到首页
        while (aft_num) {
            if (--page_num_bf <= 0) {
                break;
            }
            aft_num--;
            pagination.prepend(page_li(String(page_num_bf)));
        }
    }

    var prev = page_li("«");
    var next = page_li("»");
    pagination.prepend(prev);
    pagination.append(next);

    if (page_index === "1") {
        prev.hide();
    } else if (page_index === page_end) {
        next.hide();
    }

}

// 生成页码元素li
function page_li(page_text) {
    var li = $("<li></li>");
    if (page_text === "«") {
        li = $("<li class='prev'></li>");
    } else if (page_text === "»") {
        li = $("<li class='next'></li>");
    }
    var a = $("<a></a>");
    a.text(page_text);
    li.append(a);
    return li;
}
<!--初始化翻页组件和分类tab组件，并为之注册点击事件-->
$(document).ready(
    function () {
        // 切换结果分类标签的active状态
        $('#nav_result_cat').children().removeClass('active');
        var cat = $('#searchcat').val();
        switch (cat) {
            case 'type' :
                $('#cat_type').addClass('active');
                break;
            case 'brand' :
                $('#cat_brand').addClass('active');
                break;
            case 'model' :
                $('#cat_model').addClass('active');
                break;
            case 'fingerprint' :
                $('#cat_fingerprint').addClass('active');
                break;
        }
        // 注册点击分类tab的事件
        cat_tab_click();

        // 初始化翻页组件并设置当前页码标签设为active
        adjust_pages();
        // 为翻页组件注册点击事件
        page_li_click();

        // 为搜索按钮注册点击事件。
        $("button#btn_search").click(function () {
            get_results_post();
        });
        // 为checkedbox添加点击事件
        check_all_click();

        // 为删除按钮添加点击事件
        bt_delete_click();

        // 为修改按钮注册点击事件
        bt_edit_click();

        // 调整结果容器的高
        var height = window.innerHeight - 380;
        $('div.results_content').css("min-height", height);

    }
);
// 注册点击分类tab的事件,将对应的分类作为参数放到隐藏的input里
function cat_tab_click() {
    $('.cat').click(function () {
        var inp_searchcat = $('input#searchcat');
        switch ($(this).attr('id')) {
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

        get_results_post();
    });
}

// 注册点击页码的事件
function page_li_click() {
    $('ul.pagination li').on("click", function () {
        var inp_search_text = $("input[name='search_text']");
        var search_text = inp_search_text.val();
        var search_category = $("input[name='search_category']").val();
        var inp_page = $("input[name='page_index']");

        var page_current = inp_page.val();
        // 调整页码参数
        var page_next = $(this).text();

        if (page_next === "«") {
            page_next = parseInt(page_current) - 1;
        }
        else if (page_next === "»") {
            page_next = parseInt(page_current) + 1;
        }
        // 修改当前页码存放在隐藏input
        inp_page.val(page_next);

        adjust_pages();
        page_li_click();

        if (search_text === "") {
            search_text = $('input#searchtext_last').val();
            inp_search_text.val(search_text);
        }
        get_results(search_text, search_category, page_next);
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

// 全选函数
function check_all_click() {
    $("input[type='checkbox'][value ='-1']").on('click', function () {
        $("input[type='checkbox'][value != '-1']").click();
    });
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

// // 调用删除接口的函数
// function delete_records() {
//
// }

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
            // 切换图标
            $(this).html("<span class='glyphicon glyphicon-floppy-save'></span> 保存");
            // 将表格切换成编辑框
            $("input[type='checkbox']:checked").parent().siblings("td").each(function () {
                var text_inputs = $(this).find("input:text");
                if (!text_inputs.length) {
                    // 用 name 属性来保存原来的值，以便修改失败后恢复显示
                    $(this).html("<input type='text' class='form-control_self' " +
                        "name='" + $(this).text() + "' style='background-color: transparent' value='" + $(this).text() + "'>");

                }
            });
            // alert($("tbody tr:nth-of-type(2n)").css("color"));
        }
        else if (str === "保存") {
            // 切换图标
            $(this).html("<span class='glyphicon glyphicon-pencil'></span> 修改");
            $("tbody td input:text").each(function () {
                $(this).parent().html($(this).prop("name"));
            });
        }


    });
}
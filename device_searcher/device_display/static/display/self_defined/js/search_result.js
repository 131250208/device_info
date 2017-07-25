/**
 * Created by wycheng on 7/25/17.
 */


function append_tr(father, list_row) {
    var tr = document.createElement("tr");

    var input = document.createElement("input");
    input.type = "checkbox";
    input.style.marginRight = "5px";
    var chk_box = document.createElement("th");
    chk_box.appendChild(input);

    tr.appendChild(chk_box);
    for (var i = 0; i < list_row.length; ++i) {
        var th = document.createElement("th");
        th.innerHTML = list_row[i];
        tr.appendChild(th);
    }

    father.append(tr);
}

// 将查询结果显示到表格上
function show_intable(result_json) {
    // thead
    var thead = $('table.table thead');
    thead.empty();

    append_tr(thead, ['field_name1', 'field_name2', 'field_name3', 'field_name4'])

    // tbody
    var tbody = $("table.table tbody");
    tbody.empty();

    var list = result_json.record_list;
    for (var j = 0; j < list.length; ++j) {
        append_tr(tbody, list[j]);
    }
}


<!--用于处理结果分类的tab状态，以及点击tab改变隐藏分类input的事件和post请求-->
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
        // 当前页码标签设为active
        var page_index = $("input[name='page_index']").val();

        var li_page_current = $("ul.pagination li:eq(" + page_index + ")");
        li_page_current.siblings().removeClass('active')
        li_page_current.addClass('active');

        // 调整结果容器的高
        var height = window.innerHeight - 380;
        $('div.results_content').css("min-height", height);

    },

    // 注册点击分类tab的事件,将对应的分类作为参数放到隐藏的input里，接着发送post请求调用接口
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

        var search_text = $("input[name='search_text']").val();
        var search_category = $("input[name='search_category']").val();
        var page_index = $("input[name='page_index']").val();
        // 发送post请求调用接口
        var inp_searchtext = document.getElementById("searchtext");
        if (inp_searchtext.value === "") {
//            inp_searchtext.setCustomValidity('搜索内容不能为空，且不包含特殊字符(\\，；)。');
        } else {
            get_results(search_text, search_category, page_index);
        }
    }),
    // 注册点击页码的事件
    $('ul.pagination li').click(function () {
        var search_text = $("input[name='search_text']").val();
        var search_category = $("input[name='search_category']").val();
        var inp_page = $("input[name='page_index']");
        var page_current = inp_page.val();
        var li_page_current = $("ul.pagination li:eq(" + page_current + ")");

        // 调整页码参数
        var page_next = $(this).text();

        $(this).siblings().removeClass('active');

        if (page_next === "«") {
            page_next = parseInt(page_current) - 1;
            li_page_current.prev().addClass('active');
        }
        else if (page_next === "»") {
            page_next = parseInt(page_current) + 1;
            li_page_current.next().addClass('active');
        } else {
            // 修改当前页码为active
            $(this).addClass('active');
        }
        // 修改当前页码存放在隐藏input
        inp_page.val(page_next);


        var inp_searchtext = document.getElementById("searchtext");
        if (inp_searchtext.value === "") {
//            inp_searchtext.setCustomValidity('搜索内容不能为空，且不包含特殊字符(\\，；)。');
        } else {

            get_results(search_text, search_category, page_next);
        }
    })
);


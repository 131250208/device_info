/**
 * Created by wycheng on 8/9/17.
 */

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

// 根据当前页码调整翻页组件,当前页码标签设为active
// 初始化和调整页码的函数，after_click为点击页码后调用的函数
function adjust_pages(input_page_total, input_page_index, after_click) {
    var page_total = input_page_total.val();

    var page_index = input_page_index.val();

    var pagination = $('ul.pagination');

    pagination.empty();

    if (page_total <= 1) {
        return
    }

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

    var page_num_aft = parseInt(page_index);
    while (aft_num) {
        if (++page_num_aft > page_total) {
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
    }
    if (page_index === page_total) {
        next.hide();
    }

    // 给页码添加点击事件
    page_li_click(input_page_total, input_page_index, after_click);
}

// 注册点击页码的事件
function page_li_click(input_page_total, input_page_index, after_click) {
    $('ul.pagination li').on("click", function () {
        var inp_page = input_page_index;

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

        // 无论请求是否返回，都需要调整一次页码显示
        adjust_pages(input_page_total, input_page_index, after_click);
        // 调用点击事件后执行的函数
        after_click();
    });
}
/**
 * Created by wycheng on 8/29/17.
 */

$(document).ready(
    function () {
        //设置导航栏的元素active切换
        $("li.nav_li").attr("class", "nav_li");
        $("li#nav_statistics").addClass("active");

        // 柱状图
        var url = get_url("display:get_capacity");
        $.get(url,
            function (data, status) {
                if (status === "success") {
                    var result_json = eval('(' + data + ')');

                    new Vue({
                        el: '#histogram',
                        created: function () {
                            this.chartData = {
                                columns: ['能力方向', '总量', '品牌数量'],
                                rows: result_json
                            };
                            this.chartSettings = {
                                dimension: ['能力方向'],
                                metrics: ['总量', '品牌数量'],
                                yAxisType: ['KMB'],
                                yAxisName: ['数量'],
                                area: true,
                                stack: {
                                    '数量': ['总量', '品牌数量']
                                }
                            }
                        }
                    });
                } else {
                    Messenger().post("请求没有响应");
                }
            });


        // 展示型号中的所有的品牌的占比分布的饼图
        var url = get_url("display:get_brands_model");
        $.get(url,
            function (data, status) {
                if (status === "success") {
                    var result_json = eval('(' + data + ')');

                    new Vue({
                        el: '#brands_model_pie',
                        created: function () {
                            this.chartData = {
                                columns: ['brand_name', 'num'],
                                rows: result_json
                            };
                            this.chartSettings = {
                                legendLimit: 7,// 说明的限制数量，多于这个数就隐藏
                                limitShowNum: 5,
                                dimension: 'brand_name',
                                metrics: 'num',
                                dataType: 'KMB',
                                selectedMode: 'single',
                                hoverAnimation: true,
                                radius: 150,
                                offsetY: 200
                            };
                        }
                    });
                } else {
                    Messenger().post("请求没有响应");
                }
            });

        // 展示指纹识别的所有的品牌的占比分布的饼图
        var url = get_url("display:get_brands_fingerprint");
        $.get(url,
            function (data, status) {
                if (status === "success") {
                    var result_json = eval('(' + data + ')');

                    new Vue({
                        el: '#brands_fingerprint_pie',
                        created: function () {
                            this.chartData = {
                                columns: ['brand_name', 'num'],
                                rows: result_json
                            };
                            this.chartSettings = {
                                legendLimit: 7,
                                limitShowNum: 5,
                                dimension: 'brand_name',
                                metrics: 'num',
                                dataType: 'KMB',
                                selectedMode: 'single',
                                hoverAnimation: true,
                                radius: 150,
                                offsetY: 200
                            };
                        }
                    });
                } else {
                    Messenger().post("请求没有响应");
                }
            });
    }
);
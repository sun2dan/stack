/**
 具体用法请看 ../tools/
 * **/
window.tools = {
    getQuery: function () {
        var str = location.search;
        var obj = {};
        if (!str) {
            console.log("当前url上没有参数");
            return obj;
        }
        str.replace(/([\w\d_\-%]+)=([\w\d\/%.\-_:#]+)(\b|&|$)/gmi, function (m1, group1, group2, index, input) {
            obj[group1] = decodeURIComponent(group2);
        });
        return obj;
    },


    format: function (str) {
        var pattern = /\{([\w\-_]+)\}/gm;
        var arr = Array.prototype.slice.call(arguments, 1);
        var args = /\{(\d+)\}/.test(str) ? arr : arr[0];
        var formatStr = str.replace(pattern, function () {
            return args[arguments[1]];
        });
        return formatStr;
    }
};
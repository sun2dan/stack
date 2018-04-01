var gulp = require('gulp');
var path = require('path');
var fs = require('fs');

// Plugins
var uglify = require('gulp-uglify');
var minifyCSS = require('gulp-minify-css');
var wrapper = require('gulp-wrapper');
var replace = require('gulp-replace');
var foreach = require('gulp-foreach');
var fileinclude = require('gulp-file-include');
var rename = require("gulp-rename");

var browserSync = require('browser-sync');
var remoteSrc = require('gulp-remote-src');
var gutil = require('gulp-util');
var ftp = require('vinyl-ftp');
var gulpSequence = require('gulp-sequence');  //管理任务队列
var transport = require("gulp-seajs-transport");

/**================================================================
 Static server
 =================================================================*/
gulp.task('server', function () {
    var files = [
        '**/**/*.*'
    ];
    browserSync.init(files, {
        server: {
            baseDir: './',
            directory: true,
            https: false
        }
    });
});
var gulp = require('gulp');
var browserSync = require('browser-sync');

gulp.task('server', function () {
  var files = [
    '**/**/*.*'
  ];
  browserSync.init(files, {
    server: {
      baseDir: './',
      directory: true,
      https: false
    },
    port: 3002
  });
});


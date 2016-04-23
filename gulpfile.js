var gulp = require('gulp');
var webserver = require('gulp-webserver');

gulp.task('default', function () {
  return gulp.src('src')
    .pipe(webserver({
      livereload: true,
      open: true
    }));
});
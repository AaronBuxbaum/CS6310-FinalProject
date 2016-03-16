var gulp = require('gulp');
var concat = require('gulp-concat');
var sourcemaps = require('gulp-sourcemaps');
var del = require('del');

var BUILD_DIR = 'build';
var appJS = [
    'src/app.js',
    'src/**/*.js',
    '!src/**/*.spec.js'
];
var vendorsJS = [
    'node_modules/angular/angular.js',
    'node_modules/angular-animate/angular-animate.js',
    'node_modules/angular-aria/angular-aria.js',
    'node_modules/angular-material/angular-material.js'
];
var vendorsCSS = [
    'node_modules/angular-material/angular-material.css'
];

gulp.task('clean', function() {
  return del([BUILD_DIR]);
});

gulp.task('build:app', function() {
  return gulp.src(appJS)
    .pipe(sourcemaps.init())
    .pipe(concat('app.js'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(BUILD_DIR));
});

gulp.task('build:vendors:js', function () {
    return gulp.src(vendorsJS)
        .pipe(sourcemaps.init())
        .pipe(concat('vendors.js'))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(BUILD_DIR));
});

gulp.task('build:vendors:css', function () {
    return gulp.src(vendorsCSS)
        .pipe(sourcemaps.init())
        .pipe(concat('vendors.css'))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(BUILD_DIR));
})

gulp.task('watch', function() {
  gulp.watch(appJS, ['clean', 'build:app']);
});

gulp.task('default', ['watch', 'build:vendors:js', 'build:vendors:css', 'build:app']);
var gulp = require('gulp');
var concat = require('gulp-concat');
var webserver = require('gulp-webserver');
var sourcemaps = require('gulp-sourcemaps');
var templateCache = require('gulp-angular-templatecache');
var del = require('del');
var karma = require('karma');
var runSequence = require('run-sequence');

/*
    Data
*/
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
  'node_modules/angular-material/angular-material.js',
  'node_modules/@angular/router/angular1/angular_1_router.js'
];
var vendorsCSS = [
  'node_modules/angular-material/angular-material.css'
];


/*
    Test tasks
*/
gulp.task('test', ['test:unit']);

gulp.task('test:unit', ['build:app'], function(done) {
  new karma.Server({
    configFile: __dirname + '/karma.conf.js',
    singleRun: true
  }, done).start();
});


/*
    Build tasks
*/
gulp.task('build', ['build:app', 'build:vendors']);
gulp.task('build:app', ['build:app:js', 'build:app:css', 'build:app:html', 'copy:index']);
gulp.task('build:vendors', ['build:vendors:js', 'build:vendors:css']);

gulp.task('build:app:js', function() {
  return gulp.src(appJS)
    .pipe(sourcemaps.init())
    .pipe(concat('app.js'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(BUILD_DIR));
});

gulp.task('build:app:css', function() {
});

gulp.task('build:app:html', function() {
  return gulp.src('src/**/*.html')
    .pipe(templateCache({
      module: 'CS6310'
    }))
    .pipe(gulp.dest(BUILD_DIR));
});

gulp.task('build:vendors:js', function() {
  return gulp.src(vendorsJS)
    .pipe(sourcemaps.init())
    .pipe(concat('vendors.js'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(BUILD_DIR));
});

gulp.task('build:vendors:css', function() {
  return gulp.src(vendorsCSS)
    .pipe(sourcemaps.init())
    .pipe(concat('vendors.css'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(BUILD_DIR));
});

gulp.task('copy:index', function() {
  return gulp.src('src/index.html')
    .pipe(gulp.dest(BUILD_DIR));
});



/*
    Misc tasks
*/
gulp.task('server', function() {
  return gulp.src(BUILD_DIR)
    .pipe(webserver({
      livereload: false,
      open: true
    }));
});

gulp.task('clean', function() {
  return del([BUILD_DIR]);
});

gulp.task('watch', function() {
  gulp.watch('src/**', ['build']);
});

gulp.task('default', function(callback) {
  runSequence('clean', 'build', 'server', callback);
});
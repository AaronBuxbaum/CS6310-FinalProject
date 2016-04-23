angular.module('CS6310').factory('CourseService', function (API_URL, $http) {
  var svc = {};

  svc.getAllClasses = function () {
    return $http.get(API_URL + 'course/);
  };

  svc.getSchedule = function () {
    return $http.get(API_URL + 'schedule/');
  };

  return svc;
});
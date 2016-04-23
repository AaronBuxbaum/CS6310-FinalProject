angular.module('CS6310').factory('CourseService', function (API_URL, $http) {
  var svc = {};
  var url = API_URL + 'course/';

  svc.getAllClasses = function () {
    return $http.get(url);
  };

  return svc;
});
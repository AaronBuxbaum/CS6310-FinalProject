angular.module('CS6310').factory('InstructorService', function (API_URL, $http) {
  var svc = {};
  var url = API_URL + 'instructor/';

  svc.getClasses = function () {
    return $http.get(url);
  };

  svc.addClass = function (obj) {
    return $http.post(url, obj);
  };

  svc.deleteClass = function (obj) {
    return $http.delete(url, { params: obj });
  };

  return svc;
});
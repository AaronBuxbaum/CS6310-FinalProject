angular.module('CS6310').factory('SolverService', function (API_URL, $http) {
  var svc = {};
  var url = API_URL + 'solver/';

  svc.optimize = function () {
    return $http.post(url);
  };

  return svc;
});
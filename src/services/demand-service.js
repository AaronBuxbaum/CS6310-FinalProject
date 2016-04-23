angular.module('CS6310').factory('DemandService', function (API_URL, $http) {
  var svc = {};
  var url = API_URL + 'demand/';

  svc.getAggregate = function () {
    return $http.get(url + 'aggregate');
  };

  svc.submit = function (selectedClasses) {
    return $http.post(url, selectedClasses.map(function (item) {
      return {
        semester_id: 1,
        course_id: item.id
      };
    }));
  };

  return svc;
});
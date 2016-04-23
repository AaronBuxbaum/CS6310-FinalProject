angular.module('CS6310').factory('UserService', function (API_URL, $http) {
  var svc = {};
  var url = API_URL + 'user/';

  svc.getUser = function () {
    return $http.get(url);
  };

  svc.logIn = function (username, password) {
    return $http.post(url + 'login', {
      username: username,
      password: password
    }).then(function (response) {
      svc.loggedIn = response.data;
      return svc.loggedIn;
    });
  };

  svc.logOut = function () {
    return $http.post(url + 'logout').then(function (response) {
      svc.loggedIn = null;
      return svc.loggedIn;
    });
  };

  return svc;
});
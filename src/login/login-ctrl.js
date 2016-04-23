angular.module('CS6310').controller('LoginCtrl', function (UserService) {
  var ctrl = this;

  ctrl.logIn = function () {
    console.log('TODO');

    UserService.loggedIn = true;
    ctrl.$router.navigate(['Student Registration', { id: 0 }]);
  };
});
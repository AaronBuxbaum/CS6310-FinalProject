angular.module('CS6310').controller('LoginCtrl', function (UserService) {
  var ctrl = this;

  ctrl.logIn = function () {
    return UserService.logIn(ctrl.username, ctrl.password).then(function (userData) {
      var route = {
        'student': 'Student Registration',
        'administrator': 'Administrator Panel',
        'ta': 'Teaching Assistant'
      };

      return ctrl.$router.navigate([route[userData.role], { id: userData.id }]);
    }, function (error) {
      ctrl.errorMessage = error.statusText;
    });
  };
});
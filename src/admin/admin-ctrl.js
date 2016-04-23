angular.module('CS6310').controller('AdminCtrl', function () {
    var ctrl = this;

    ctrl.$routerOnActivate = function () {
        return UserService.loggedIn.role === 'administrator';
    };
});
angular.module('CS6310').controller('AdminCtrl', function (UserService) {
    var ctrl = this;

    ctrl.$routerCanActivate = function () {
        return UserService.getUser().then(function (user) {
            return user.data.role === 'administrator';
        });
    };
});
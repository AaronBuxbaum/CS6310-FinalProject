angular.module('CS6310').component('login', {
    templateUrl: 'login/login.html',
    controller: 'LoginCtrl',
    bindings: {
        $router: '<'
    }
});
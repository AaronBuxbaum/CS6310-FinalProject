angular.module('CS6310').component('main', {
    templateUrl: 'main/main.html',
    controller: 'MainCtrl',
    bindings: {
        text: '@'
    }
});
angular.module('CS6310').component('classItem', {
    templateUrl: 'registration/class-item.html',
    controller: 'ClassItemCtrl',
    bindings: {
        ngModel: '<'
    }
});
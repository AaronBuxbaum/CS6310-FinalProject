angular.module('CS6310').component('classItem', {
    templateUrl: 'class-item/class-item.html',
    controller: 'ClassItemCtrl',
    bindings: {
        ngModel: '<'
    }
});
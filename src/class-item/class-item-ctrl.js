angular.module('CS6310').controller('ClassItemCtrl', function () {
    var ctrl = this;

    ctrl.getFullClassName = function (obj) {
        return obj.subject + ' ' + obj.number;
    };
});
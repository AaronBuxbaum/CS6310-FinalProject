angular.module('CS6310').controller('FooterCtrl', function ($rootRouter) {
    var ctrl = this;

    ctrl.aboutUs = function () {
        $rootRouter.navigate('aboutUs');
    };
});
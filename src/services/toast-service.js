angular.module('CS6310').factory('ToastService', function ($toast) {
  var svc = {};

  svc.showToast = function (text, action, position) {
    var toast = $mdToast.simple()
      .textContent(text)
      .action(action || 'OK')
      .highlightAction(true)
      .position(position);
    return $mdToast.show(toast);
  };

  return svc;
});
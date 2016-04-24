angular.module('CS6310').factory('ToastService', function ($mdToast) {
  var svc = {};

  svc.showToast = function (text, action) {
    var toast = $mdToast.simple()
      .textContent(text)
      .action(action || 'OK')
      .highlightAction(true)
    return $mdToast.show(toast);
  };

  return svc;
});
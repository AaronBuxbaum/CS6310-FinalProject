angular.module('CS6310').controller('RegistrationCtrl', function ($scope, $filter, UserService, CourseService) {
  var ctrl = this;

  if (!UserService.loggedIn) {
    ctrl.$router.navigate(['Log In']);
  }

  CourseService.getAllClasses().then(function (response) {
    console.log(response.data.courses);
    ctrl.allClasses = response.data.courses[0];
    ctrl.selectedClasses = _.sampleSize(ctrl.allClasses, 4);
    ctrl.allClasses.map(function (item, i) {
      item.image = '//loremflickr.com/50/50?random=' + i;
      return item;
    });
  });

  //Actual Functionality
  ctrl.querySearch = function (query) {
    return $filter('filter')(ctrl.allClasses, query);
  };

  ctrl.selectClass = function (item) {
    return ctrl.selectedClasses.push(item);
  };

  ctrl.isSelected = function (item) {
    return ctrl.selectedClasses.indexOf(item) < 0;
  };

  ctrl.submitChanges = function () {
    return DemandService.submit(ctrl.selectedClasses);
  };
});
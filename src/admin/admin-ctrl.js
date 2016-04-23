
angular.module('CS6310').controller('AdminCtrl', function ($scope, $filter, UserService, CourseService, DemandService) {
    var ctrl = this;

  if (!UserService.loggedIn) {
    //this.router  = new router();
    ctrl.$router.navigate(['Log In']);
  }

  CourseService.getAllClasses().then(function (response) {
    console.log(response.data.courses);
    ctrl.allClasses = response.data.courses[0].map(function (item, i) {
      item.image = '//loremflickr.com/50/50?random=' + i;
      return item;
    });
    DemandService.getDemand().then(function (response) {
      var id = response.data.demand[0].course.id;
      ctrl.selectedClasses = [_.find(ctrl.allClasses, { id: id })];
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
    return DemandService.submitDemand(ctrl.selectedClasses);
  };
});
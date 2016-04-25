angular.module('CS6310').controller('RegistrationCtrl', function (
  $scope,
  $filter,
  UserService,
  CourseService,
  DemandService,
  SolverService,
  ToastService
) {
  var ctrl = this;
  ctrl.selectedClasses = [];

  ctrl.$routerOnActivate = function () {
    UserService.getUser().then(function (user) {
      if (user.data.role !== 'student') {
        ctrl.$router.navigate(['Log In']);
      }
    });
  };

  CourseService.getAllClasses().then(function (response) {
    ctrl.allClasses = response.data.courses[0];

    DemandService.getDemand().then(function (response) {
      response.data.demand.map(function (item) {
        return item.course.id;
      }).forEach(function (id) {
        ctrl.selectedClasses.push(_.find(ctrl.allClasses, { id: id }));
      });
    });
  });

  ctrl.querySearch = function (query) {
    return $filter('filter')(ctrl.allClasses, query);
  };

  ctrl.selectClass = function (item) {
    return ctrl.selectedClasses.push(item);
  };

  ctrl.isSelected = function (item) {
    return ctrl.selectedClasses.indexOf(item) < 0;
  };

  ctrl.setSchedule = function () {
    CourseService.getSchedule().then(function (response) {
      ctrl.schedule = response.data.schedule;
    });
  };
  ctrl.setSchedule();

  ctrl.submitChanges = function () {
    return DemandService.submitDemand(ctrl.selectedClasses)
      .then(SolverService.optimize)
      .then(function () {
        return ToastService.showToast('Class Registration completed!');
      })
      .then(ctrl.setSchedule);
  };
});
angular.module('CS6310').component('main', {
    templateUrl: 'main/main.html',
    controller: 'MainCtrl',
    $routeConfig: [
      {
        path: '/login',
        name: 'TODO',
        component: 'login',
        useAsDefault: true
      },
      {
        path: '/student/:id',
        name: 'Student',
        component: 'student'
      }
    ]
});
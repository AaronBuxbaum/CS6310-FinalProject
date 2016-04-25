angular.module('CS6310', [
  'ngMaterial',
  'ngMdIcons',
  'ngComponentRouter'
])

  .value('$routerRootComponent', 'main')
  .value('API_URL', '/api/')

  .config(function ($mdThemingProvider) {
    $mdThemingProvider.theme('default')
      .primaryPalette('yellow')
      .dark();
  });
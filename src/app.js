angular.module('CS6310', [
  'ngMaterial',
  'ngMdIcons',
  'ngComponentRouter'
])

  .value('$routerRootComponent', 'main')
  .value('API_URL', 'http://192.168.99.104/api/')

  .config(function ($mdThemingProvider) {
    $mdThemingProvider.theme('default')
      .primaryPalette('yellow')
      .dark();
  });
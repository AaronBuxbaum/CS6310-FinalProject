angular.module('CS6310', [
  'ngMaterial',
  'ngMdIcons',
  'ngComponentRouter'
])

  .value('$routerRootComponent', 'main')

  .config(function ($mdThemingProvider) {
    $mdThemingProvider.theme('default')
      .primaryPalette('yellow')
      .dark();
  });
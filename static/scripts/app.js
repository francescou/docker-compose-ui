'use strict';

/**
 * @ngdoc overview
 * @name composeUiApp
 * @description
 * # composeUiApp
 *
 * Main module of the application.
 */
angular
  .module('composeUiApp', [
    'ngResource',
    'ngRoute'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl'
      })
      .when('/project/:id', {
        templateUrl: 'views/project.html',
        controller: 'ProjectCtrl'
      })
      .when('/project/:id/:container', {
        templateUrl: 'views/container.html',
        controller: 'ContainerCtrl'
      })
      .when('/create', {
        templateUrl: 'views/create.html',
        controller: 'CreateCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  })
  .filter('trim', function () {
    return function (s, n) {
      var sTrim = s.trim();
      var sLimit = sTrim.substring(0, n);
      return sLimit.length < sTrim.length ? sLimit + '...' : sLimit;
    };

  });

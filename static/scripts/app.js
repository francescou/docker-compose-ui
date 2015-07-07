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
      .otherwise({
        redirectTo: '/'
      });
  });

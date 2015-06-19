'use strict';

/**
 * @ngdoc overview
 * @name staticApp
 * @description
 * # staticApp
 *
 * Main module of the application.
 */
angular
  .module('staticApp', [
    'ngResource',
    'ngRoute'
  ], function($provide, $httpProvider) {

  $httpProvider.interceptors.push(function($q, $rootScope) {
    return {
      responseError: function(rejection) {
        window.alert('HTTP error code: ' + rejection.status);
        $rootScope.working = false;
        return $q.reject(rejection);
      }
    };
  });

})
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });

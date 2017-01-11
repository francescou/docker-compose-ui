'use strict';

/**
 * @ngdoc function
 * @name composeUiApp.controller:ProjectCtrl
 * @description
 * # ProjectCtrl
 * Controller of the composeUiApp
 */
angular.module('composeUiApp')
  .controller('ProjectCtrl', function ($scope, $routeParams) {

      $scope.id = $routeParams.id;

  });

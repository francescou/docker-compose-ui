'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:ProjectCtrl
 * @description
 * # ProjectCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('ProjectCtrl', function ($scope, $routeParams) {

    $scope.id = $routeParams.id;

  });

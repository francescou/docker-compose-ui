'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('MainCtrl', function ($scope, $resource) {

    var Projects = $resource('api/v1/projects');
    $scope.projects = Projects.get();

  });

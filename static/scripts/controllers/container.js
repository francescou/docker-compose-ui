'use strict';

/**
 * @ngdoc function
 * @name composeUiApp.controller:ContainerCtrl
 * @description
 * # ContainerCtrl
 * Controller of the composeUiApp
 */
angular.module('composeUiApp')
  .controller('ContainerCtrl', function ($scope, $routeParams, $resource) {

      var Container = $resource('api/v1/projects/:id/:container');

      var project = $routeParams.id;
      $scope.project = project;

      Container.get({id: project, container: $routeParams.container}, function (data) {
          $scope.container = data;
      });

  });

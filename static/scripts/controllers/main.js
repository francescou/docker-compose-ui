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

    $resource('api/v1/host').get(function (data) {
      $scope.dockerHost = data.host.split(':')[0];
    });

    function reload() {
      $scope.projects = Projects.get();
    }

    $scope.reload = reload;

    $scope.isEmpty = function (obj) {
      return angular.equals({}, obj);
    };

    reload();

  });

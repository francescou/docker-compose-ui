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

    function reload(init) {
      Projects.get(function (data) {
        $scope.projects = data;
        if (!init) {
          alertify.success('reloadeded ' + Object.keys(data.projects).length + ' projects');
        }
      });
    }

    $scope.reload = reload;

    $scope.isEmpty = function (obj) {
      return angular.equals({}, obj);
    };

    reload(true);

  });

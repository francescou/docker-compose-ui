'use strict';

/**
 * @ngdoc function
 * @name composeUiApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the composeUiApp
 */
angular.module('composeUiApp')
  .controller('MainCtrl', function ($scope, $resource) {

    var Projects = $resource('api/v1/projects');

    function reload(init) {
      Projects.get(function (data) {
        $scope.projects = data;
        if (!init) {
          alertify.success(Object.keys(data.projects).length + ' projects reloadeded');
        }
      });
    }

    $scope.reload = reload;

    $scope.isEmpty = function (obj) {
      return angular.equals({}, obj);
    };

    reload(true);

  });

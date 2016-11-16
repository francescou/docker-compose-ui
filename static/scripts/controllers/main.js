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

    $scope.isActive = function (id, l) {
      var name = id.toLowerCase().replace(/\-/g, '');
      return l.indexOf(name) >= 0;
    };

    function reload(displayMessage) {
      Projects.get(function (data) {
        $scope.projects = data;
        if (displayMessage) {
          alertify.success(Object.keys(data.projects).length + ' projects reloaded');
        }
      });
    }

    $scope.reload = reload;

    $scope.isEmpty = function (obj) {
      return angular.equals({}, obj);
    };

    reload(false);

  });

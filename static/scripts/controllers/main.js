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
      var host = data.host.split(':')[0];
      $scope.dockerHost = host;
      alertify.log('Host: ' + host);
    });

    function reload(init) {
      Projects.get(function (data) {
        $scope.projects = data;
        if (!init) {
          alertify.log('reloadeded ' + Object.keys(data.projects).length + ' projects');
        }
      });
    }

    $scope.reload = reload;

    $scope.isEmpty = function (obj) {
      return angular.equals({}, obj);
    };

    reload(true);

  });

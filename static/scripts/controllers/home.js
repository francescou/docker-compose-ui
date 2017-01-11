'use strict';

/**
 * @ngdoc function
 * @name composeUiApp.controller:HomeCtrl
 * @description
 * # HomeCtrl
 * Controller of the composeUiApp
 */
angular.module('composeUiApp')
  .controller('HomeCtrl', function ($scope, $resource) {

      var Host = $resource('api/v1/host');

      var label = 'local Unix socket';

      $scope.unixSocket = label;

      Host.get(function (data) {
          alertify.success('Docker Host: ' + (data.host || label));
          $scope.dockerHost = data.host;
          $scope.workdir = data.workdir;
      });

      $scope.select = function ($event, host) {
          if (host === undefined) {
              $event.preventDefault();
          }
          alertify.success('set Docker Host: ' + (host || label));
          Host.save({id:host || null});
          $scope.dockerHost = host;
      };

  });

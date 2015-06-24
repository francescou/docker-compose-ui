'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:HomeCtrl
 * @description
 * # HomeCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('HomeCtrl', function ($scope, $resource) {

    function setHost(host) {
      alertify.log('Host: ' + host);
      $scope.dockerHost = host;
    }

    $resource('api/v1/host').get(function (data) {
      var host = data.host.split(':')[0];
      setHost(host);
      $scope.hosts = [host];
    });

    $scope.select = setHost;

    $scope.add = function(h) {
      $scope.hosts.push(h);
    };

  });

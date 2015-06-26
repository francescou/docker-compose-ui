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

    var Host = $resource('api/v1/host');

    function setHost(host) {
      alertify.success('Docker Host: ' + host);
      $scope.dockerHost = host;
      Host.save({id:host});
    }

    Host.get(function (data) {
      var host = data.host.split(':')[0];
      setHost(host);
      $scope.hosts = [host];
    });

    $scope.select = setHost;

    $scope.add = function(h) {
      $scope.hosts.push(h);
    };

  });

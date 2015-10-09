'use strict';

/**
 * @ngdoc function
 * @name composeUiApp.controller:CreateCtrl
 * @description
 * # CreateCtrl
 * Controller of the composeUiApp
 */
angular.module('composeUiApp')
  .controller('CreateCtrl', function ($scope, $routeParams, $resource, $location) {

    var Projects = $resource('api/v1/projects', null, {
      'create': {
        url: 'api/v1/create',
        method: 'POST'
      }
    });

    $scope.create = function (name, yml) {

      //TODO: check if name is alphanumeric
      Projects.create({
        name: name,
        yml: yml
      }, function (data) {
        alertify.success('created project: ' + name + ', path: ' + data.path);
        $scope.$parent.reload();
        $location.path('project/' + name);

      }, function (err) {
        alertify.alert(err.data);
      });


    };


  });

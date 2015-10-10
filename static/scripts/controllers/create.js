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

    var Search = $resource('api/v1/search');
    var Yml = $resource('api/v1/yml');

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


    $scope.search = function (query) {

      Search.save({
        query: query
      }, function (res) {
        $scope.items = res.items;
      }, function (res) {
        alertify.alert('search error: ' + res.data.error);
      });

    };

    $scope.load = function (name, id) {

      Yml.save({
        id: id
      }, function (data) {
        $scope.yml = data.content;
      });
      $scope.name = name;
      $scope.items = [];
    };


  });

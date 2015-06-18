'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('MainCtrl', function ($scope, $resource, $rootScope) {

    var Projects = $resource('api/v1/projects');
    $scope.projects = Projects.get();

    var Project = $resource('api/v1/projects/:id', null, {
      'update': { method:'PUT' }
    });

    var Logs = $resource('api/v1/logs/:id/:limit');

    function refresh (key) {
      $scope.project = Project.get({id: key});
    }

    $scope.kill = function (project) {
      $rootScope.working = true;
      Project.delete({id: project}, function () {
        $scope.output = project + ' killed';
        refresh(project);
        $rootScope.working = false;
      });
    };
    $scope.pull = function (project) {
      $rootScope.working = true;
      Project.update({id: project}, function () {
        $scope.output = 'pull ok: ' + project;
        $rootScope.working = false;
      });
    };
    $scope.up = function (project) {
      $rootScope.working = true;
      Project.save({id: project}, function (data) {
        $scope.output = data.containers.length + ' container(s) started';
        refresh(project);
        $rootScope.working = false;
      });
    };

    $scope.displayLogs = function (project) {
      $scope.logs = Logs.get({id:project, limit: 100});
    }

    $scope.select = function (id) {
      delete $scope.output;
      delete $scope.logs;
      $scope.active = id;
      refresh(id);
    }

  });

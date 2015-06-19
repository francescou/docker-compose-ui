'use strict';

angular.module('staticApp')
  .directive('actions', function ($resource) {

    return {
      restrict: 'E',
      scope: {
        project: '=',
        output: '=',
        projectId: '=',
        working: '=',
        logs: '='
      },
      templateUrl: 'views/actions.html',
      controller: function($scope) {

        var Project = $resource('api/v1/projects/:id', null, {
          'update': { method:'PUT' }
        });

        var Logs = $resource('api/v1/logs/:id/:limit');

        $scope.kill = function () {
          $scope.working = true;
          var id = $scope.projectId;
          Project.delete({id: id}, function () {
            $scope.output = 'killed';
            $scope.working = false;
            $scope.project = Project.get({id: id});
          });
        };
        $scope.pull = function () {
          $scope.working = true;
          Project.update({id: $scope.projectId}, function () {
            $scope.output = 'pull terminated';
            $scope.working = false;
          });
        };
        $scope.up = function () {
          $scope.working = true;
          var id = $scope.projectId;
          Project.save({id: id}, function (data) {
            $scope.output = data.containers.length + ' container(s) started';
            $scope.working = false;
            $scope.project = Project.get({id: id});
          });
        };

        $scope.displayLogs = function () {
          $scope.logs = Logs.get({id: $scope.projectId, limit: 100});
        };


      }
    };
  });
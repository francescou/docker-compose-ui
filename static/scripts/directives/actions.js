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
      link: function (scope, element, attrs) {

      },
      controller: function($scope, $element, $attrs, $transclude) {

        var Project = $resource('api/v1/projects/:id', null, {
          'update': { method:'PUT' }
        });

        var Logs = $resource('api/v1/logs/:id/:limit');

        $scope.kill = function () {
          $scope.working = true;
          Project.delete({id: $scope.projectId}, function () {
            $scope.output = 'killed';
            $scope.working = false;
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
          Project.save({id: $scope.projectId}, function (data) {
            $scope.output = data.containers.length + ' container(s) started';
            $scope.working = false;
          });
        };

        $scope.displayLogs = function () {
          $scope.logs = Logs.get({id: $scope.projectId, limit: 100});
        };


      }
    };
  });
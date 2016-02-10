'use strict';

angular.module('composeUiApp')
  .directive('actions', function ($resource, projectService, logService) {

    return {
      restrict: 'E',
      scope: {
        services: '=',
        projectId: '=',
        working: '='
      },
      templateUrl: 'views/actions.html',
      controller: function($scope) {

        var Project = $resource('api/v1/projects/:id', null, {
          'update': { method:'PUT' },
          'build': {
            url: 'api/v1/build',
            method: 'POST'
          },
          'start': {
            url: 'api/v1/start',
            method: 'POST'
          },
          'stop': {
            url: 'api/v1/stop',
            method: 'POST'
          },
          'down': {
            url: 'api/v1/down',
            method: 'POST'
          }
        });

        var Logs = $resource('api/v1/logs/:id/:limit');

        $scope.kill = function () {
          var id = $scope.projectId;
          updateProjectStatus(Project.delete, id + ' killed');
        };
        $scope.pull = function () {
          $scope.working = true;
          var id = $scope.projectId;
          Project.update({id: id}, function () {
            alertify.success(id + ' pull terminated');
            $scope.working = false;
          }, function (err) {
            $scope.working = false;
            alertify.alert(err.data);
          });
        };
        $scope.up = function () {
          updateProjectStatus(Project.save, 'project is up');
        };
        $scope.down = function () {
          updateProjectStatus(Project.down, 'project is down');
        };

        $scope.start = function () {
          updateProjectStatus(Project.start, 'project started');
        };

        $scope.stop = function () {
          updateProjectStatus(Project.stop, 'project stopped');
        };

        function updateProjectStatus(fn, msg) {
          $scope.working = true;
          var id = $scope.projectId;
          fn({id: id}, function () {
            alertify.success(msg);
            $scope.working = false;
            Project.get({id: id}, function (data) {
              $scope.services = projectService.groupByService(data);
            });
          }, function (err) {
            $scope.working = false;
            alertify.alert(err.data);
          });

        }


        $scope.build = function () {
          $scope.working = true;
          var id = $scope.projectId;
          Project.build({id: id}, function () {
            alertify.success(id + ' build terminated');
            $scope.working = false;
          }, function (err) {
            $scope.working = false;
            alertify.alert(err.data);
          });
        };


        $scope.combinedLogs = function () {
          Logs.get({id: $scope.projectId, limit: 100}, function (data) {
            $scope.logs = logService.formatLogs(data.logs);
            $scope.showCombinedLogsDialog = true;
          });
        };

        $scope.scrollToBottom = function () {
          var objDiv = $(".combined-logs")[0];
          objDiv.scrollTop = objDiv.scrollHeight;
        };

      }
    };
  });

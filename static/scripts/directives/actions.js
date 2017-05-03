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
                  'create': {
                      url: 'api/v1/_create',
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
                  },
                  'restart': {
                      url: 'api/v1/restart',
                      method: 'POST'
                  }
              });

              var Logs = $resource('api/v1/logs/:id/:limit');

              $scope.kill = function () {
                  var id = $scope.projectId;
                  updateProjectStatus(Project.delete, id + ' killed');
              };
              $scope.restart = function () {
                  var id = $scope.projectId;
                  updateProjectStatus(Project.restart, id + ' restarted');
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
                  updateProjectStatus(Project.save, 'project up');
              };
              $scope.down = function () {
                  updateProjectStatus(Project.down, 'project down');
              };

              $scope.create = function () {
                  updateProjectStatus(Project.create, 'project created');
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
                      $scope.$parent.$parent.reload(false);
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


              $scope.lineLimit = 80;
              $scope.combinedLogs = function () {

                  Logs.get({id: $scope.projectId, limit: $scope.lineLimit}, function (data) {
                      $scope.logs = logService.formatLogs(data.logs);
                      $scope.showCombinedLogsDialog = true;
                  });
              };

              $scope.scrollToBottom = function () {
                  var objDiv = $('.combined-logs')[0];
                  objDiv.scrollTop = objDiv.scrollHeight;
              };

          }
      };
  });

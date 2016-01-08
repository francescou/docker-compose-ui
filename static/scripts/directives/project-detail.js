'use strict';

angular.module('composeUiApp')
  .directive('projectDetail', function($resource, $log, projectService, $window){
    return {
      restrict: 'E',
      scope: {
        projectId: '=',
        path: '='
      },
      templateUrl: 'views/project-detail.html',
      controller: function($scope) {

        var Project = $resource('api/v1/projects/:id');
        var Host = $resource('api/v1/host');
        var Yml = $resource('api/v1/projects/yml/:id');

        $scope.$watch('projectId', function (val) {
          if (val) {
            $log.debug('refresh ' + val);
            Project.get({id: val}, function (data) {
              $scope.services = projectService.groupByService(data);
            }, function (err) {
              alertify.alert(err.data);
            });

            Host.get(function (data) {
              var host = data.host;
              $scope.hostName = host ? host.split(':')[0] : null;
            });
          }

        });

        var Logs = $resource('api/v1/logs/:id/:container/:limit');

        $scope.displayLogs = function (id) {
          Logs.get({id: $scope.projectId, limit: 100, container: id}, function (data) {
            $scope.containerLogs = id;
            $scope.showDialog = true;
            $scope.logs = data.logs;
          });
        };

        var Service = $resource('api/v1/services', null, {
          scale: {
            method: 'PUT'
          }
        });

        $scope.scale = function (service) {
          var num = $window.prompt('how many instances of service ' + service + '?');

          $scope.working = true;

          Service.scale({service: service, project: $scope.projectId, num: num}, function () {

            Project.get({id: $scope.projectId}, function (data) {
              $scope.services = projectService.groupByService(data);
              $scope.working = false;
            }, function (err) {
              $scope.working = false;
              alertify.alert(err.data);
            });

          }, function (err) {
            $scope.working = false;
            alertify.alert(err.data);
          });
        };


        $scope.isEmpty = function (obj) {
          return angular.equals({}, obj);
        };

        $scope.yml = function () {
          Yml.get({
            id: $scope.projectId
          }, function (data) {
            $scope.ymlData = data.yml;
          });

        };

      }
    };
  });

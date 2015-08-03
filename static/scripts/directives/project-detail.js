'use strict';

angular.module('composeUiApp')
  .directive('projectDetail', function($resource, $log){
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

        $scope.$watch('projectId', function (val) {
          if (val) {
            $log.debug('refresh ' + val);
            Project.get({id: val}, function (data) {
              $scope.project = data;
            }, function (err) {
              alertify.alert(err.data);
            });

            Host.get(function (data) {
              var host = data.host;
              $scope.hostName = host ? host.split(':')[0] : 'localhost';
            });
          }

        });

        var Logs = $resource('api/v1/logs/:id/:limit');

        $scope.displayLogs = function (id) {
          Logs.get({id: $scope.projectId, limit: 100}, function (data) {
            $scope.showDialog = true;
            $scope.logs = data.logs[id];
          });
        };


      }
    };
  });
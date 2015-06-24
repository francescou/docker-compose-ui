'use strict';

angular.module('staticApp')
  .directive('actions', function ($resource) {

    return {
      restrict: 'E',
      scope: {
        project: '=',
        projectId: '=',
        working: '=',
        logs: '='
      },
      templateUrl: 'views/actions.html',
      controller: function($scope) {

        var Project = $resource('api/v1/projects/:id', null, {
          'update': { method:'PUT' },
          'build': {
            url: 'api/v1/build',
            method: 'POST'
          }
        });

        var Logs = $resource('api/v1/logs/:id/:limit');

        $scope.kill = function () {
          $scope.working = true;
          var id = $scope.projectId;
          Project.delete({id: id}, function () {
            alertify.log(id + ' killed');
            $scope.working = false;
            $scope.project = Project.get({id: id});
          }, function (err) {
            $scope.working = false;
            alertify.alert(err.data);
          });
        };
        $scope.pull = function () {
          $scope.working = true;
          var id = $scope.projectId;
          Project.update({id: id}, function () {
            alertify.log(id + ' pull terminated');
            $scope.working = false;
          }, function (err) {
            $scope.working = false;
            alertify.alert(err.data);
          });
        };
        $scope.up = function () {
          $scope.working = true;
          var id = $scope.projectId;
          Project.save({id: id}, function (data) {
            alertify.log(data.containers.length + ' container(s) started');
            $scope.working = false;
            $scope.project = Project.get({id: id});
          }, function (err) {
            $scope.working = false;
            alertify.alert(err.data);
          });
        };

        $scope.displayLogs = function () {
          $scope.logs = Logs.get({id: $scope.projectId, limit: 100});
        };

        $scope.build = function () {
          $scope.working = true;
          var id = $scope.projectId;
          Project.build({id: id}, function () {
            alertify.log(id + ' build terminated');
            $scope.working = false;
          }, function (err) {
            $scope.working = false;
            alertify.alert(err.data);
          });
        };


      }
    };
  });
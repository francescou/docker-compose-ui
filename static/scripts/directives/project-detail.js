'use strict';

angular.module('staticApp')
  .directive('projectDetail', function($resource, $log){
    return {
      restrict: 'E',
      scope: {
        projectId: '=',
        path: '=',
        dockerHost: '='
      },
      templateUrl: 'views/project-detail.html',
      controller: function($scope) {

        var Project = $resource('api/v1/projects/:id');

        $scope.$watch('projectId', function (val) {
          if (val) {
            $log.debug('refresh ' + val);
            Project.get({id: val}, function (data) {
              $scope.project = data;
            }, function (err) {
              alertify.alert(err.data);
            });
          }

        });
      }
    };
  });
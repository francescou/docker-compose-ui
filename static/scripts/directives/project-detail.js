'use strict';

angular.module('staticApp')
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

        $scope.$watch('projectId', function (val) {
          if (val) {
            $log.debug('refresh ' + val);
            $scope.project = Project.get({id: val});
          }

        });
      }
    };
  });
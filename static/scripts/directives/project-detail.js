'use strict';

angular.module('staticApp')
  .directive('projectDetail', function($resource, $log){
    return {
      restrict: 'E',
      scope: {
        projectId: '=',
        path: '=',
        highlighted: '='
      },
      templateUrl: 'views/project-detail.html',
      controller: function($scope) {

        var Project = $resource('api/v1/projects/:id');

        $scope.$watch('highlighted', function (val) {
          if (val) {
            var id = $scope.projectId;
            $log.debug('refresh ' + id);
            $scope.project = Project.get({id: id});
          }

        });
      }
    };
  });
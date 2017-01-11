'use strict';

angular.module('composeUiApp')
  .factory('projectService', function () {

      return {
          groupByService: function (data) {
              return _.groupBy(data.containers, 'labels[\'com.docker.compose.service\']');
          }
      };
  });
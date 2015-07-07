'use strict';

angular.module('composeUiApp')
  .filter('filterByName', function () {
    return function (projects, query) {

      var filteredProjects;

      if (query) {

        filteredProjects = _.chain(projects)
          .map(function (path, name) {
            return {
              name: name,
              path: path
            };
          })
          .filter(function (item) {
            return item.name.indexOf(query) >= 0;
          })
          .map(function (item) {
            return [item.name, item.path];
          })
          .object()
          .value();

      } else {
        filteredProjects = projects;
      }

      return filteredProjects;
    };
  });
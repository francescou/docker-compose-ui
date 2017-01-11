'use strict';

angular.module('composeUiApp')
  .factory('logService', function () {

      function omitTimestamp(f) {

          var colors = [];

          return _.map(f, function (item) {

              var id = item.container;

              if (colors.indexOf(id) < 0) {
                  colors.push(id);
              }

              return {
                  text: item.text.split(' ').splice(1).join(' '),
                  container: id,
                  color: colors.indexOf(id)
              };
          });
      }

      function sortByDate(data) {
          return data.sort(function (a,b) {
              if(a.text < b.text) {
                  return -1;
              } else if(a.text > b.text) {
                  return 1;
              } else {
                  return 0;
              }
          });
      }

      function excludeBlankLines(lines) {
          return _.filter(lines, function (line) {
              return line.text.trim().length > 0;
          });
      }

      function addContainerInfo(combinedLogs) {
          return _.map(combinedLogs, function (lines, containerId) {
              return _.map(lines, function (line) {
                  return {
                      text: line,
                      container: containerId
                  };
              });
          });
      }

      var formatLogs = _.flowRight(omitTimestamp,
      sortByDate,
      excludeBlankLines,
      _.flatten,
      addContainerInfo);

      return {
          formatLogs: formatLogs
      };
  });
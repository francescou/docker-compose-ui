'use strict';

angular.module('staticApp')
  .directive('log', function () {

    return {
      restrict: 'E',
      scope: {
        logData: '='
      },
      template: '<pre ng-show="logData" class="text-left logs">{{logData.join("\n")}}</pre>',
      link: function (scope, element, attrs) {

        scope.$watch('logData', function (v) {
          scope.$applyAsync(function () {
            var pre = element.children()[0];
            pre.scrollTop = pre.scrollHeight;
          });
        })
      }
    };
  });
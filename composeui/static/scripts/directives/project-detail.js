'use strict';

angular.module('composeUiApp')
  .directive('projectDetail', function($resource, $log, projectService, $rootScope){
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
              $scope.hostName = host ? host.split(':')[0] : 'localhost';
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
          alertify.prompt('how many instances of service ' + service + '?', function (e, num) {

            if (e) {
              $scope.working = true;

              Service.scale({service: service, project: $scope.projectId, num: num}, function () {
                $scope.working = false;
              }, function (err) {
                $scope.working = false;
                alertify.alert(err.data);
              });
            }

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

        var routeChangeSuccess = $rootScope.$eventToObservable('$routeChangeSuccess');

        Rx.DOM.fromEventSource('/subscribe')
          .map(function (json) {
            return JSON.parse(json.data);
          }).groupBy(function (x) {
          return x.metadata['com.docker.compose.project'];
        }, function (x) {
          return x;
        }).subscribe(function (obs) {

          var route = $scope.projectId.replace(/-/g, ''); //TODO: hack

          if (obs.key === route) {

            obs
              .throttle(1000)
              .delay(1000)
              .subscribe(function (data) {
                $log.debug(data);
                Project.get({id: $scope.projectId}, function (data) {
                  $scope.services = projectService.groupByService(data);
                });
              });

          } else {
            obs.map(function (e) {
              var service = e.metadata['com.docker.compose.service'];
              var number = e.metadata['com.docker.compose.container-number'];
              var msg = service + '-' + number + ' ' + e.status;
              return msg;
            })
              .windowWithTime(3000)
              .selectMany(function (x) {
                return x.toArray();
              }).filter(function (e) {
                return e.length > 1;
              }).takeUntil(routeChangeSuccess)
              .subscribe(function (msg) {
                alertify.log([].concat('<b>' + obs.key + '</b>').concat(msg).join('<br>'));
              });

          }

        });

      }
    };
  });

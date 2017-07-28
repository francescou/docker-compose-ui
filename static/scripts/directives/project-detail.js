'use strict';

angular.module('composeUiApp')
  .directive('projectDetail', function($resource, $log, projectService, $window, $location, $timeout){
      return {
          restrict: 'E',
          scope: {
              projectId: '=',
              path: '='
          },
          templateUrl: 'views/project-detail.html',
          controller: function($scope) {

              var Project = $resource('api/v1/projects/:id', null, {
                  remove: {
                      method: 'DELETE',
                      url: 'api/v1/remove-project/:id'
                  }
              });


              var Host = $resource('api/v1/host');
              var Yml = $resource('api/v1/projects/yml/:id');
              var Readme = $resource('api/v1/projects/readme/:id');

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
                          $scope.hostName = host ? host.split(':')[0] : null;
                      });

                      Readme.get({
                          id: $scope.projectId
                      }, function (data) {
                          $scope.readme = data.readme;
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

              var Exec = $resource('api/v1/exec/:container/:id');

              $scope.showRunCommand = function (container) {
                  $scope.container = container;
                  $scope.showRunDialog = true;
              };
              $scope.runCommand = function (container_id, command) {
                  Exec.save({
                      container: container_id
                  }, {
                      command: command 
                  }, function(r) {
                      alertify.success('`' + r.command + '` running in ' + r.container + '.');

                      // repeatedly check exec command exit code
                      var checkExec = function() {
                          // check for successful exit code
                          Exec.get({
                              container: container_id,
                              id: r.id
                          }, function (exec) {
                              if (exec.running) {
                                  // keep checking until the command is finished
                                  return $timeout(checkExec, 5000);
                              }

                              if (exec.code === 0) {
                                  alertify.success('`' + r.command + '` successfully completed in ' + r.container + '.');
                              } else {
                                  alertify.error('`' + r.command + '` exited with non-zero exit code');
                              }
                          });
                      };
                      checkExec();
                  }, function() {
                      alertify.error('Error running `' + command + '`');
                  });
              };

              $scope.rebuild = function(serviceName) {
                  $scope.working = true;
                  Project.save({id: $scope.projectId, service_names: [serviceName], do_build: true},
            function () {
                $scope.working = false;
                alertify.success(serviceName + ' rebuild successful.');
            },
            function (err) {
                $scope.working = false;
                alertify.alert(err.data);
            });
              };

              var Service = $resource('api/v1/services', null, {
                  scale: {
                      method: 'PUT'
                  }
              });

              $scope.scale = function (service) {
                  alertify.prompt('how many instances of service ' + service + '?', 1, function (evt, num) {

                      if (!isNaN(num)) {
                          $scope.working = true;

                          Service.scale({service: service, project: $scope.projectId, num: num}, function () {

                              Project.get({id: $scope.projectId}, function (data) {
                                  $scope.services = projectService.groupByService(data);
                                  $scope.working = false;
                              }, function (err) {
                                  $scope.working = false;
                                  alertify.alert(err.data);
                              });

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

              $scope.details = function () {
                  Yml.get({
                      id: $scope.projectId
                  }, function (data) {
                      $scope.yml = data.yml;
                      $scope.env = data.env;
                      $scope.config = data.config;
                  });

              };


              $scope.deleteProject = function (id) {
                  alertify.confirm('Do you really want to remove project ' + id + '?', function (rm) {
                      if (rm) {
                          Project.remove({
                              id: id
                          }, function () {
                              alertify.message('deleted ' + id);
                              $scope.$parent.reload(false);
                              $location.path('/');
                          }, function (r) {
                              alertify.error('cannot delete ' + id + ': ' + r.data);
                          });
                      }
                  });
              };


          }
      };
  })
  .directive('markdown', function() {
      return {
          restrict: 'AE',
          scope: {
              status: '='
          },
          link: function (scope, element, attrs) {
              var md_content = attrs.content;
              var html_content = markdown.toHTML(md_content);
              $(html_content).appendTo(element);
          }
      };
  });

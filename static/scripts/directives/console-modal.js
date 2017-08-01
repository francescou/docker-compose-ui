'use strict';

angular.module('composeUiApp')
    .directive('consoleModalShow', function ($parse) {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {

                //Hide or show the modal
                scope.showConsoleModal = function (visible, elem) {
                    if (!elem)
                        elem = element;

                    if (visible)
                        $(elem).modal('show');
                    else
                        $(elem).modal('hide');
                };

                //Watch for changes to the modal-visible attribute
                scope.$watch(attrs.consoleModalShow, function (newValue) {
                    scope.showConsoleModal(newValue, attrs.$$element);
                });

                //Update the visible value when the dialog is closed through UI actions (Ok, cancel, etc.)
                $(element).bind('hide.bs.modal', function () {
                    $parse(attrs.consoleModalShow).assign(scope, false);
                    if (!scope.$$phase && !scope.$root.$$phase)
                        scope.$apply();
                });
            }

        };
    });
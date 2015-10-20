'use strict';

var app = angular.module('sensorship', ['ngRoute', 'ngTable']);

angular.module('sensorship').config(['$locationProvider', '$routeProvider', '$provide',
    function($locationProvider, $routeProvider, $provide) {

      // The sniffer decorator enables hashbang compatibility in older browsers,
      // while html5 history rewriting mode is enabled.
      $provide.decorator('$sniffer', function($delegate) {
        $delegate.history = false;
        return $delegate;
      });
      $locationProvider.html5Mode(true).hashPrefix('!');

      $routeProvider

	  // route for the Home page
      .when('/', {
        templateUrl : 'static/pages/home.html',
        controller : 'homeCtrl',
      })

      // route for the Nodes page
      .when('/nodes/', {
        templateUrl : 'static/pages/nodes.html',
        controller : 'allNodesCtrl',
      })

      // route for each individual Node page
      .when('/node/:name', {
        templateUrl : 'static/pages/node.html',
        controller : 'nodeCtrl',
      })

	  // route for the apps page
      .when('/containers/', {
        templateUrl : 'static/pages/containers.html',
        controller : 'containerCtrl',
      })

      .otherwise({
        redirectTo: '/'
      });
    }]);


// Nav bar active setting
var cleanAll = function() {
	$("#homebutton").removeClass("active");
	$("#nodesbutton").removeClass("active");
	$("#containersbutton").removeClass("active");
};

$(document).ready(function() {
	$("#homebutton").click(function() {
		cleanAll();
		$("#homebutton").addClass("active");
	});

	$("#nodesbutton").click(function() {
		cleanAll();
		$("#nodesbutton").addClass("active");
	});

	$("#containersbutton").click(function() {
		cleanAll();
		$("#containersbutton").addClass("active");
	});
});


angular.module('sensorship').controller('homeCtrl', function($scope, $http) {

	$scope.submitTask = function() {
		var image = $('#taskimage').val();
		var mappings = $('#taskmappings').val();

		payload = {"image" : image, "mappings":mappings};

		var res = $http.post("/submit", payload)
		res.success(function(data, status, headers, config) {
			$('#taskimage').val('');
			$('#taskmappings').val('');
			$scope.sync(true);
		});

	};

	$scope.sync = function(apply) {
		$.getJSON("/tasks", function(data) {
			if (apply) {
				$scope.$apply(function() {
					$scope.items = data;
				});
			} else {
				$scope.items = data;
			}
		});
	}

	$scope.toggle = function(id, state) {
		id = '{"id": "' + id + '"}';
		if (state == "on") {
			var res = $http.post("/off", id);
			res.success(function(data, status, headers, config) {
				$scope.sync(true);
			});
		} else {
			var res = $http.post("/on", id);
			res.success(function(data, status, headers, config) {
				$scope.sync(true);
			});
		}
	};

	$scope.sync(false);
});


angular.module('sensorship').controller('allNodesCtrl', function($scope, $http) {
	$scope.registerNode = function() {
		var nodename = $('#nodename').val();
		var nodeip = $('#nodeip').val();
		var mappings = $('#pinmappings').val();

		payload = {"nodename" : nodename, 
					"nodeip" : nodeip,
					"mappings" : mappings
		};

		var res = $http.post("/register", payload);
		res.success(function(data, status, headers, config) {
			$('#nodename').val('');
			$('#pinmappings').val('');
			$scope.sync(true);
		});
	};

	$scope.sync = function(apply) {
		$.getJSON("/nodes", function(data) {
			if (apply) {
				$scope.$apply(function() {
					$scope.items = data;
				});
			} else {
				$scope.items = data;
			}
		});
	}
});


angular.module('sensorship').controller('nodeCtrl', function($scope) {
});

angular.module('sensorship').controller('containerCtrl', function($scope) {
});

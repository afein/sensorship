
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
			$('#error').hide();
		});
		res.error(function(data, status, headers, config) {
			if (status == "400") {
				$('#error').html($(data)[5].outerHTML);
				$('#error').show();
			}
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


angular.module('sensorship').controller('allNodesCtrl', function($scope, $http, $interval) {
	$scope.registerNode = function() {
		var name = $('#nodename').val();
		var ip = $('#nodeip').val();
		var mappings = $('#pinmappings').val();

		payload = {"name" : name, 
					"ip" : ip,
					"mappings" : mappings
		};

		var res = $http.post("/register", payload);
		res.success(function(data, status, headers, config) {
			$('#nodename').val('');
			$('#nodeip').val('');
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

	$.getJSON("/sensors", function(data) {
		$scope.sensors = data;
	});

	$scope.sync(false);

	$scope.refresh = $interval(function() {
		$scope.sync(true);
	}, 6000);

	$scope.$on('$destroy', function () {
		$interval.cancel($scope.refresh);
	});
});


angular.module('sensorship').controller('monitoringCtrl', function($scope, $interval) {
	$scope.sync = function(apply) {
		$.getJSON("/nodes", function(data) {
			if (apply) {
				$scope.$apply(function() {
					$scope.items = data;
				});
			} else {
				$scope.items = data;
			}
			console.log($scope.items);
		});
	}

	$scope.sync(true);

	$scope.refresh = $interval(function() {
		$scope.sync(true);
	}, 3000);

	$scope.$on('$destroy', function () {
		$interval.cancel($scope.refresh);
	});

});
